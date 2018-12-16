import asyncio
import time
from worker_images import config, nats_client


def load_conf(config_file):
    """
    Load configuration from config file

    :return:
    """
    conf = config.load_config(config_file)
    return conf


def test_nats_run():
    """
    Test connection to NATS without TLS
    """
    conf = load_conf("tests/config/config_tests.ini")

    # Start NATS loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(nats_client.run(loop, conf))
    loop.close()


def test_nats_run_tls():
    """
    Test connection to NATS with TLS
    """
    conf = load_conf("tests/config/config_tests_tls.ini")

    # Start NATS loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(nats_client.run(loop, conf))
    loop.close()
