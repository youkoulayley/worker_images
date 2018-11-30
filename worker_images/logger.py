import logging
from worker_images import config

application_name = config.get_config("DEFAULT", "application_name")
log_level = config.get_config("LOGGING", "level")


def init_logging():
    handler_console = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s : %(message)s')
    handler_console.setFormatter(formatter)
    logger = logging.getLogger(application_name)
    logger.addHandler(handler_console)

    if log_level == "info":
        logger.setLevel(logging.INFO)
    elif log_level == "warning":
        logger.setLevel(logging.WARNING)
    elif log_level == "error":
        logger.setLevel(logging.ERROR)
    elif log_level == "debug":
        logger.setLevel(logging.DEBUG)

