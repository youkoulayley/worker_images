import pytest
import os
import errno
import urllib.error
import urllib.request as curl
from worker_images import worker, config

application_name = config.get_config("DEFAULT", "application_name")
original_folder = config.get_config("DEFAULT", "original_folder")
images_folder = config.get_config("DEFAULT", "images_folder")
image_formats = config.get_config("DEFAULT", "image_formats")

if not os.path.exists(original_folder):
    try:
        os.makedirs(original_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


@pytest.mark.parametrize("message", [
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl_banner", "crop_type": "banner",
      "crop": "middle", "force_crop": False}),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "crop_type": "poster",
      "crop": "top", "force_crop": True})
])
def test_decode_message(message):
    """
    Test to decode message

    :param message:
    """
    assert worker.decode_message(message)


@pytest.mark.parametrize("message, error_expected", [
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "crop_type": "poster",
      "crop": "top", "force_rop": True}, KeyError)
])
def test_decode_message_fail(message, error_expected):
    """
    Test unavailable message

    :param message:
    :param error_expected:
    """
    with pytest.raises(error_expected):
        worker.decode_message(message)


@pytest.mark.parametrize("image, error_expected", [
    ({"url": "https://www.thetvdb.com/banners/text/95759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "middle", "force_crop": True}, curl.HTTPError),
    ({"url": "toto://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "middle", "force_crop": True}, curl.URLError)
])
def test_retrieve_image_fail(image, error_expected):
    with pytest.raises(error_expected):
        worker.retrieve_image(image)


@pytest.mark.parametrize("image", [
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "middle", "force_crop": True})
])
def test_retrieve_image(image):
    assert worker.retrieve_image(image)


@pytest.mark.parametrize("path, return_expected", [
    (original_folder + "/supergirl.jpg", True),
    (original_folder + "/toto.jpg", False)
])
def test_check_file_exists(path, return_expected):
    assert worker.check_file_exists(path) == return_expected


@pytest.mark.parametrize("file, md5_expected", [
    (original_folder + "/supergirl.jpg", "f278c2bece6f8b0cff0754cab0ddda2b"),
])
def test_check_md5_local_file(file, md5_expected):
    assert worker.check_md5(open(file, 'rb')) == md5_expected


@pytest.mark.parametrize("file, error_expected", [
    (original_folder + "/toto.jpg", Exception),
])
def test_check_md5_local_file_fail(file, error_expected):
    with pytest.raises(error_expected):
        worker.check_md5(open(file, 'rb'))


@pytest.mark.parametrize("url, md5_expected", [
    ("https://www.thetvdb.com/banners/text/295759-2.jpg", "f278c2bece6f8b0cff0754cab0ddda2b"),
])
def test_check_md5_url(url, md5_expected):
    assert worker.check_md5(curl.urlopen(url)) == md5_expected


@pytest.mark.parametrize("image, image_format, return_expected", [
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "top", "force_crop": True}, "300_10", True),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "middle", "force_crop": True}, "300_10", True),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "bottom", "force_crop": True}, "300_10", True),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "toto", "force_crop": True}, "300_10", False),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "top", "force_crop": True}, "85_200", True),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "middle", "force_crop": True}, "85_200", True),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "bottom", "force_crop": True}, "120_120", True),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "toto", "force_crop": True}, "120_120", False),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "toto", "force_crop": True}, "758_140", True),
])
def test_resize_and_crop(image, image_format, return_expected):
    assert worker.resize_and_crop(image, image_format) == return_expected


@pytest.mark.parametrize("message, return_expected", [
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg",
      "name": "supergirl_banner2", "crop_type": "banner", "crop": "middle", "force_crop": False}, True),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg",
      "name": "supergirl_banner2", "crop_type": "banner", "crop": "middle", "force_crop": True}, True),
    ({"url": "https://www.thetvdb.com/banners/graphical/295759-g9.jpg",
      "name": "supergirl_banner2", "crop_type": "banner", "crop": "middle", "force_crop": True}, True),
    ({"url": "https://www.thetvdb.com/banners/graphical/295759-g9.jpg",
      "name": "supergirl_banner2", "crop_type": "poster", "crop": "middle", "force_crop": False}, True),
    ({"url": "https://www.thetvdb.com/banners/graphical/295759-g9.jpg",
      "name": "supergirl_banner2", "crop_type": "poster", "crop": "middle", "force_crop": False}, True)
])
def test_run(message, return_expected):
    assert worker.run(message) == return_expected


@pytest.mark.parametrize("message,error_expected", [
    ({"url": "https://www.thetvdb.com/banners/text/29559-2.jpg",
      "name": "supergirl_banner2", "crop_type": "banner", "crop": "middle", "force_crop": False},
     urllib.error.HTTPError),
    ({"url": "toto://www.thetvdb.com/banners/text/295759-2.jpg",
      "name": "supergirl_banner2", "crop_type": "banner", "crop": "middle", "force_crop": False},
     urllib.error.URLError)
])
def test_run_fail(message, error_expected):
    with pytest.raises(error_expected):
        worker.run(message)
