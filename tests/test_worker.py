import pytest
import os
import urllib.error
from worker_images import worker, config


def load_app():
    """
    Load application (configuration + object worker_images)

    :return:
    """
    conf = config.load_config("config_tests.ini")
    worker_image = worker.WorkerImage(conf)

    # Setup directory
    if not os.path.exists(conf.get('DEFAULT', 'original_folder')):
        os.makedirs(conf.get('DEFAULT', 'original_folder'))

    return worker_image


@pytest.mark.parametrize("message", [
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg",
      "name": "supergirl_banner", "crop_type": "banner", "crop": "middle", "force_crop": False}),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg",
      "name": "supergirl_banner", "crop_type": "banner", "crop": "middle", "force_crop": True}),
    ({"url": "https://www.thetvdb.com/banners/graphical/295759-g9.jpg",
      "name": "supergirl_banner", "crop_type": "banner", "crop": "middle", "force_crop": True}),
    ({"url": "https://www.thetvdb.com/banners/posters/5bd458bda1772.jpg",
      "name": "supergirl", "crop_type": "poster", "crop": "middle", "force_crop": False}),
    ({"url": "https://www.thetvdb.com/banners/posters/5bd458bda1772.jpg",
      "name": "supergirl", "crop_type": "poster", "crop": "middle", "force_crop": False}),
    ({"url": "https://www.thetvdb.com/banners/posters/5bd458bda1772.jpg",
      "name": "supergirl", "crop_type": "poster", "crop": "top", "force_crop": True}),
    ({"url": "https://www.thetvdb.com/banners/posters/5bd458bda1772.jpg",
      "name": "supergirl", "crop_type": "poster", "crop": "bottom", "force_crop": True}),
    ({"url": "https://www.thetvdb.com/banners/posters/5bd458bda1772.jpg",
      "name": "supergirl", "crop_type": "poster2", "crop": "bottom", "force_crop": False})
])
def test_run(message):
    """
    Tests run function

    :param message:
    """
    worker_image = load_app()
    assert worker_image.run(message)


@pytest.mark.parametrize("message,error_expected", [
    ({"url": "https://www.thetvdb.com/banners/text/29559-2.jpg",
      "name": "supergirl_banner2", "crop_type": "banner", "crop": "middle", "force_crop": False},
     urllib.error.HTTPError),
    ({"url": "toto://www.thetvdb.com/banners/text/295759-2.jpg",
      "name": "supergirl_banner2", "crop_type": "banner", "crop": "middle", "force_crop": False},
     urllib.error.URLError),
    ({"url": "https://www.thetvdb.com/banners/text/29559-2.jpg",
      "name": "supergirl_banner", "crop_type": "banner", "crop": "middle", "force_crop": False},
     urllib.error.HTTPError),
    ({"url": "toto://www.thetvdb.com/banners/text/295759-2.jpg",
      "name": "supergirl_banner", "crop_type": "banner", "crop": "middle", "force_crop": False},
     urllib.error.URLError),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg",
      "nae": "supergirl_banner2", "crop_type": "banner", "crop": "middle", "force_crop": False},
     KeyError),
    ({"url": "https://www.thetvdb.com/banners/posters/5bd458bda1772.jpg",
      "name": "supergirl", "crop_type": "poster", "crop": "toto", "force_crop": True},
     ValueError),
    ({"url": "https://www.thetvdb.com/banners/text/295759-2.jpg",
      "name": "supergirl_banner2", "crop_type": "banner", "crop": "toto", "force_crop": True},
     ValueError),
])
def test_run_fail(message, error_expected):
    """
    Tests when the run function failed

    :param message:
    :param error_expected:
    """
    worker_image = load_app()

    with pytest.raises(error_expected):
        worker_image.run(message)
