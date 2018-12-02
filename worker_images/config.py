import configparser


def get_config(section, key):
    """
    Get a key in a section of the config file.

    :param section:
    :param key:
    :return:
    """

    config = configparser.ConfigParser()
    config.read('../config.ini')

    value = config.get(section, key)

    return value
