import asyncio
import pytest
from worker_images import config, nats_client


def load_conf():
    """
    Load configuration from config file

    :return:
    """
    conf = config.load_config("config_tests.ini")
    return conf


def test_nats_run():
    conf = load_conf()

    # Start NATS loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(nats_client.run(loop, conf))
    loop.close()
