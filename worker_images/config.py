import configparser
import logging
import sys
from pathlib import Path

logger = logging.getLogger("worker_images")


def init_config():
    config = configparser.ConfigParser()
    config_file = Path("../config.ini")
    if config_file.is_file():
        config.read('config.ini')
    else:
        sys.exit("No config file found.")

