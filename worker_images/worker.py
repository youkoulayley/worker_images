import logging
import traceback
from worker_images import config

application_name = config.get_config("DEFAULT", "application_name")
logger = logging.getLogger(application_name)


def run(message):
    logger.info("Start working")
    decode_message(message)
    logger.info("End working")


def decode_message(message):
    try:
        image = {
            'url': str(message['url']),
            # 'name': str(message['name']),
            # 'extension': str(message['url']).rsplit('.', 1)[1],
            # 'format': str(message['format']),
            # 'crop': str(message['crop'])
        }

    except (ValueError, KeyError):
        logger.error(message + " is not a valid JSON message.")
