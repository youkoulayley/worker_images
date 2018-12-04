import configparser
import os


def get_config(section, key):
    """
    Get a key in a section of the config file.

    :param section:
    :param key:
    :return:
    """

    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.abspath(__file__)) + '/../config.ini')

    value = config.get(section, key)

    return value
