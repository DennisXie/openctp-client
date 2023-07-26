import pytest
from pytest_mock import MockerFixture

from openctp_client.objects import CtpConfig


@pytest.fixture
def config():
    conf = CtpConfig("tcp://test_address", "borker_id", "auth_code", "appi_id", "", "")
    return conf


@pytest.fixture
def spi_callback(mocker: MockerFixture):
    return mocker.stub(name="spi_callback")
