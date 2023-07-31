import pytest
from pytest_mock import MockerFixture

from openctp_client.apis import TdAPI, MdAPI
from openctp_client.objects import CtpConfig


@pytest.fixture
def config():
    conf = CtpConfig("tcp://test_address", "tcp://test_md_address", "borker_id", "auth_code", "appi_id", "", "")
    return conf


@pytest.fixture
def spi_callback(mocker: MockerFixture):
    return mocker.stub(name="spi_callback")


@pytest.fixture
def td_client(config: CtpConfig, mocker: MockerFixture):
    tdapi = mocker.patch("openctp_client.apis.td_api.tdapi")
    api = mocker.Mock(name="api")
    tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi.return_value = api
    return TdAPI(config)


@pytest.fixture
def md_client(config: CtpConfig, mocker: MockerFixture):
    mdapi = mocker.patch("openctp_client.apis.md_api.mdapi")
    api = mocker.Mock(name="api")
    mdapi.CThostFtdcMdApi.CreateFtdcMdApi.return_value = api
    return MdAPI(config)
