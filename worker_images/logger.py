import logging


def init_logging(log_level):
    """
    Init the logger for the app
    """

    handler_console = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s : %(message)s')
    handler_console.setFormatter(formatter)
    logger = logging.getLogger('worker_images')
    logger.addHandler(handler_console)

    if log_level == "info":
        logger.setLevel(logging.INFO)
    elif log_level == "warning":
        logger.setLevel(logging.WARNING)
    elif log_level == "error":
        logger.setLevel(logging.ERROR)
    elif log_level == "debug":
        logger.setLevel(logging.DEBUG)
    else:
        raise ValueError
