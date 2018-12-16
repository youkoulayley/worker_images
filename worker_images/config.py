import configparser
import os


def load_config(file):
    """
    Load configuration file

    :param file:
    :return:
    """
    config = configparser.ConfigParser()
    if os.path.isfile(file):
        config.read(file)
    else:
        raise FileNotFoundError

    return config
