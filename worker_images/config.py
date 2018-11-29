import configparser


def get_config(section, key):
    config = configparser.ConfigParser()
    config.read('../config.ini')

    value = config.get(section, key)

    return value
