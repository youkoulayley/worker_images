import hashlib
import logging
import json
import os
import urllib.request as curl
import urllib.error
import math
from PIL import Image
from worker_images import config

application_name = config.get_config("DEFAULT", "application_name")
original_folder = config.get_config("DEFAULT", "original_folder")
images_folder = config.get_config("DEFAULT", "images_folder")
image_formats = config.get_config("DEFAULT", "image_formats")
logger = logging.getLogger(application_name)


def run(message):
    """
    Principal function of the worker.
    See worflow for more informations.

    :param message:
    """
    image = decode_message(message)
    image_exists = check_file_exists(original_folder + "/" + image["name"] + "." + image["extension"])

    if not image_exists:
        logger.debug("The image %s does not exist on disk. Downloading it...", image['name'])
        retrieve_image(image)
    else:
        image_path = original_folder + "/" + image['name'] + "." + image['extension']
        logger.debug("The image %s exists on disk. Checking the md5 of the file on disk and with URL...", image['name'])
        md5_file_exists = check_md5(open(image_path, 'rb'))
        try:
            md5_file_url = check_md5(curl.urlopen(image['url']))
            if md5_file_exists != md5_file_url:
                logger.info("The image %s is not the same as the one on the disk. Downloading it...", image['name'])
                retrieve_image(image)
            else:
                logger.debug("The image %s is the same as the one on the disk", image['url'])
        except urllib.error.HTTPError:
            logger.error("The URL %s does not exists.", image['url'])
            raise
        except urllib.error.URLError:
            logger.error("The URL %s is not valid", image['url'])
            raise

    for image_format in json.loads(image_formats)[image['crop_type']]:
        if image['force_crop']:
            resize_and_crop(image, image_format)
        else:
            check_crop_exists = check_file_exists(images_folder + '/' + image_format + "/" + image['name'] + "." +
                                                  image['extension'])
            if not check_crop_exists:
                resize_and_crop(image, image_format)
            else:
                logger.debug("The image %s was not resized and crop (%s).", image['name'], image_format)
    return True


def decode_message(message) -> dict:
    """
    The decode_message function is the function called when the worker want to decoade a message in JSON.
    This function return an error if one parameter is missing.

    :param message: The Redis message
    :return:
    :rtype: None
    """

    try:
        image = {
            'url': str(message['url']),
            'name': str(message['name']),
            'extension': str(message['url']).rsplit('.', 1)[1],
            'crop_type': str(message['crop_type']),
            'crop': str(message['crop']),
            'force_crop': bool(message['force_crop'])
        }
        return image

    except KeyError as e:
        logger.error("%s is not a valid JSON message. Missing : %s key.", message, e)
        raise


def retrieve_image(image: dict):
    """
    The retrieve_image function is the function called when the worker want to download an image.

    :param image: The image informations
    :return:
    """

    image_path = original_folder + "/" + image['name'] + "." + image['extension']

    try:
        curl.urlretrieve(image['url'], image_path)
        image['force_crop'] = True
        return True

    except (curl.URLError, curl.HTTPError):
        logger.error("%s cannot be retrieved.", image['url'])
        raise


def check_file_exists(path):
    """
    Function that check if a file exists

    :param path:
    :return: bool
    """

    if not os.path.exists(path):
        return False
    else:
        return True


def check_md5(file):
    """
    Check MD5 sum of file.

    :param file:
    :return:
    """

    md5 = hashlib.md5()
    while True:
        data = file.read(2 ** 20)
        if not data:
            break
        md5.update(data)

    return md5.hexdigest()


def resize_and_crop(image, image_format):
    """
    Resize and crop an image to fit the specified size.

    :param image: path for the image to resize.
    :param image_format: format to resize.

    raises:
        Exception: if can not open the file in img_path of there is problems
            to save the image.
        ValueError: if an invalid `crop_type` is provided.
    """

    # Create the folder of the resizing format
    folder_format = images_folder + '/' + image_format

    if not os.path.exists(folder_format):
        os.mkdir(folder_format)

    size = image_format.split('_')
    size[0] = int(size[0])
    size[1] = int(size[1])

    # If height is higher we resize vertically, if not we resize horizontally
    img = Image.open(original_folder + '/' + image['name'] + '.' + image['extension'])
    # Get current and desired ratio for the images
    img_ratio = img.size[0] / float(img.size[1])
    ratio = size[0] / float(size[1])
    # The image is scaled/cropped vertically or horizontally depending on the ratio
    if ratio > img_ratio:
        img = img.resize((size[0], math.floor(size[0] * img.size[1] / img.size[0])),
                         Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if image['crop'] == 'top':
            box = (0, 0, img.size[0], size[1])
        elif image['crop'] == 'middle':
            box = (0, (img.size[1] - size[1]) / 2, img.size[0], (img.size[1] + size[1]) / 2)
        elif image['crop'] == 'bottom':
            box = (0, img.size[1] - size[1], img.size[0], img.size[1])
        else:
            logger.error('%s is invalid value for crop_type', image['crop'])
            return False
        img = img.crop(box)
    elif ratio < img_ratio:
        img = img.resize((math.floor(size[1] * img.size[0] / img.size[1]), size[1]),
                         Image.ANTIALIAS)
        # Crop in the top, middle or bottom
        if image['crop'] == 'top':
            box = (0, 0, size[0], img.size[1])
        elif image['crop'] == 'middle':
            box = ((img.size[0] - size[0]) / 2, 0, (img.size[0] + size[0]) / 2, img.size[1])
        elif image['crop'] == 'bottom':
            box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
        else:
            logger.error('%s is invalid value for crop_type', image['crop'])
            return False
        img = img.crop(box)
    else:
        img = img.resize((size[0], size[1]),
                         Image.ANTIALIAS)
    # If the scale is the same, we do not need to crop
    img.save(folder_format + '/' + image['name'] + '.jpg')
    logger.info('The image %s has been resize in %s', image['name'], image_format)
    return True
