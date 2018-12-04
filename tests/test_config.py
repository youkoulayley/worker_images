import pytest
import configparser
from worker_images import config


@pytest.mark.parametrize("section,key", [
    ("DEFAULT", "application_name"),
    ("DEFAULT", "images_folder"),
    ("DEFAULT", "original_folder"),
    ("DEFAULT", "image_formats"),
    ("LOGGING", "level"),
    ("NATS", "cluster_id"),
    ("NATS", "channel"),
])
def test_get_config(section: object, key: object):
    """
    Test to get mandatory parameters

    :param section:
    :param key:
    """
    assert config.get_config(section, key)


@pytest.mark.parametrize("section, key, error_expected", [
    ("TOTO", 'titi', configparser.NoSectionError),
    ("DEFAULT", 'tata', configparser.NoOptionError)
])
def test_get_config_fail(section: object, key: object, error_expected: object):
    """
    Test unavailable section and key parameters

    :param section:
    :param key:
    :param error_expected:
    """
    with pytest.raises(error_expected):
        config.get_config(section, key)
