import logging
import traceback
from worker_images import config

application_name = config.get_config("DEFAULT", "application_name")
logger = logging.getLogger(application_name)


def run(message):
    decode_message(message)


def decode_message(message):
    try:
        image = {
            'url': str(message['url']),
            # 'name': str(message['name']),
            # 'extension': str(message['url']).rsplit('.', 1)[1],
            # 'format': str(message['format']),
            # 'crop': str(message['crop'])
        }

    except KeyError as e:
        logger.error("%s is not a valid JSON message. Missing: %s key.", message, e)
    except ValueError as e:
        logger.error('toto')
