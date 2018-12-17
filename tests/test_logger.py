import pytest
from worker_images import logger, config


def load_conf():
    """
    Load configuration from config file

    :return:
    """
    conf = config.load_config("tests/config/config_tests.ini")
    return conf


@pytest.mark.parametrize("log_level", [
    load_conf().get('LOGGING', 'level'),
    "info",
    "warning",
    "error",
    "debug"
])
def test_init_logger(log_level):
    """
    Test the init of the logger
    """

    logger.init_logging(log_level)


def test_init_logger_fail():
    """
    Test when the valuer for log level is unavailable
    """
    with pytest.raises(ValueError):
        logger.init_logging('toto')
