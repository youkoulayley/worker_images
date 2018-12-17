import asyncio
import pytest
from worker_images import config, nats_client


def load_conf(config_file):
    """
    Load configuration from config file

    :return:
    """
    conf = config.load_config(config_file)
    return conf


@pytest.mark.parametrize('config_file', [
    'tests/config/config_tests.ini',
    'tests/config/config_tests_tls.ini'
])
def test_nats_run(config_file):
    """
    Test connection to NATS without TLS
    """
    conf = load_conf(config_file)

    # Start NATS loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(nats_client.run(loop, conf))
