import pytest
from worker_images import config


@pytest.mark.parametrize("file, error_expected", [
    ('tests/config/toto.ini', FileNotFoundError)
])
def test_load_config_fail(file, error_expected):
    """
    Test unavailable section and key parameters

    :param file:
    :param error_expected:
    """
    with pytest.raises(error_expected):
        config.load_config(file)


@pytest.mark.parametrize("file", [
    'tests/config/config_tests.ini',
    'tests/config/config_tests_tls.ini'
])
def test_load_config(file):
    """
    Test available file

    :param file:
    """
    assert config.load_config(file)
