import pytest
import urllib.request as curl
from worker_images import worker


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


@pytest.mark.parametrize("image", [
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "middle", "force_crop": True})
])
def test_retrieve_image(image):
    assert worker.retrieve_image(image)


@pytest.mark.parametrize("image, error_expected", [
    ({"url": "https://www.thetvdb.com/banners/text/95759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "middle", "force_crop": True}, curl.HTTPError),
    ({"url": "toto://www.thetvdb.com/banners/text/295759-2.jpg", "name": "supergirl", "extension": "jpg",
      "crop_type": "poster", "crop": "middle", "force_crop": True}, curl.URLError)
])
def test_retrieve_image_fail(image, error_expected):
    with pytest.raises(error_expected):
        worker.retrieve_image(image)


@pytest.mark.parametrize("path, return_expected", [
    ("images/original/supergirl.jpg", True),
    ("images/original/toto.jpg", False)
])
def test_check_file_exists(path, return_expected):
    assert worker.check_file_exists(path) == return_expected


@pytest.mark.parametrize("file, md5_expected", [
    ("images/original/supergirl.jpg", "a385ae814a29320b9feb000dd42c10da"),
])
def test_check_md5_local_file(file, md5_expected):
    assert worker.check_md5(open(file, 'rb')) == md5_expected


@pytest.mark.parametrize("url, md5_expected", [
    ("https://www.thetvdb.com/banners/text/295759-2.jpg", "f278c2bece6f8b0cff0754cab0ddda2b"),
])
def test_check_md5_url(url, md5_expected):
    assert worker.check_md5(curl.urlopen(url)) == md5_expected


@pytest.mark.parametrize("image, image_format", [
    ("images/original/supergirl.jpg", "100_50"),
])
def test_resize_and_crop(image, image_format):
    assert worker.resize_and_crop(image, image_format)
