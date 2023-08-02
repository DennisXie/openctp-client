import pytest
from pytest_mock import MockerFixture

from openctp_client.clients import SimpleCtpClient
from openctp_client.objects import CtpConfig


@pytest.fixture
def mock_td_md(mocker: MockerFixture):
    tdapi = mocker.patch("openctp_client.apis.td_api.tdapi")
    tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi.return_value = mocker.Mock(name="tdapi")
    mdapi = mocker.patch("openctp_client.apis.md_api.mdapi")
    mdapi.CThostFtdcMdApi.CreateFtdcMdApi.return_value = mocker.Mock(name="mdapi")


@pytest.fixture
def simple_ctp_client(config: CtpConfig, mock_td_md):
    return SimpleCtpClient(config)


def test_should_create_simple_ctp_client(config: CtpConfig):
    client = SimpleCtpClient(config)
    assert client is not None
    assert client.tdapi is not None
    assert client.mdapi is not None


@pytest.mark.skip(reason="not implemented")
def test_should_call_api_Init_when_connect(simple_ctp_client):
    simple_ctp_client.connect()
    simple_ctp_client.tdapi.api.Init.assert_called_once()
    simple_ctp_client.mdapi.api.Init.assert_called_once()


@pytest.mark.skip(reason="not implemented")
def test_should_connected_when_connect(simple_ctp_client):
    simple_ctp_client.connect()
    # assert simple_ctp_client.connected is True
