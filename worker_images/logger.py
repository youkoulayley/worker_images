import logging
from worker_images import config

application_name = config.get_config("DEFAULT", "application_name")
log_level = config.get_config("LOGGING", "level")


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'WARNING': 33,
        'INFO': 32,
        'DEBUG': 36,
        'CRITICAL': 31,
        'ERROR': 31
    }

    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        record.msg = '\033[1;%dm%s\033[0m' % (self.COLORS[record.levelname], record.msg)
        return super(ColoredFormatter, self).format(record)


def init_logging():
    handler_console = logging.StreamHandler()
    formatter = ColoredFormatter('[%(asctime)s] %(message)s')
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

