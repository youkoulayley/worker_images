import logging


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
    logger = logging.getLogger('worker_images')
    logger.addHandler(handler_console)
    logger.setLevel(logging.INFO)
