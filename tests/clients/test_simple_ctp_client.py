import pytest
from pytest_mock import MockerFixture

from openctp_client.clients import SimpleCtpClient
from openctp_client.exceptions import CtpException
from openctp_client.objects import CtpConfig
from openctp_client.openctp import tdapi


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


def test_should_connected_is_True_when_connect(simple_ctp_client: SimpleCtpClient):
    login_field = tdapi.CThostFtdcRspUserLoginField()
    simple_ctp_client.mdapi.api.Init.side_effect = simple_ctp_client.mdapi.OnFrontConnected
    simple_ctp_client.mdapi.api.ReqUserLogin.side_effect = lambda *args: simple_ctp_client.mdapi.OnRspUserLogin(login_field, None, 2, True)
    
    simple_ctp_client.tdapi.api.Init.side_effect = simple_ctp_client.tdapi.OnFrontConnected
    simple_ctp_client.tdapi.api.ReqAuthenticate.side_effect = lambda *args: simple_ctp_client.tdapi.OnRspAuthenticate(None, None, 1, True)
    simple_ctp_client.tdapi.api.ReqUserLogin.side_effect = lambda *args: simple_ctp_client.tdapi.OnRspUserLogin(login_field, None, 2, True)
    simple_ctp_client.connect()
    
    assert simple_ctp_client.connected is True


def test_should_throw_exception_when_connect_given_md_login_failed(simple_ctp_client: SimpleCtpClient):
    login_field = tdapi.CThostFtdcRspUserLoginField()
    rsp_info = tdapi.CThostFtdcRspInfoField()
    rsp_info.ErrorID = 1
    rsp_info.ErrorMsg = "error"
    simple_ctp_client.mdapi.api.Init.side_effect = simple_ctp_client.mdapi.OnFrontConnected
    simple_ctp_client.mdapi.api.ReqUserLogin.side_effect = lambda *args: simple_ctp_client.mdapi.OnRspUserLogin(None, rsp_info, 2, True)
    
    simple_ctp_client.tdapi.api.Init.side_effect = simple_ctp_client.tdapi.OnFrontConnected
    simple_ctp_client.tdapi.api.ReqAuthenticate.side_effect = lambda *args: simple_ctp_client.tdapi.OnRspAuthenticate(None, None, 1, True)
    simple_ctp_client.tdapi.api.ReqUserLogin.side_effect = lambda *args: simple_ctp_client.tdapi.OnRspUserLogin(login_field, None, 2, True)
    
    with pytest.raises(CtpException):
        simple_ctp_client.connect()
    assert simple_ctp_client.connected is False


def test_should_throw_exception_when_connect_give_td_login_failed(simple_ctp_client: SimpleCtpClient):
    login_field = tdapi.CThostFtdcRspUserLoginField()
    simple_ctp_client.mdapi.api.Init.side_effect = simple_ctp_client.mdapi.OnFrontConnected
    simple_ctp_client.mdapi.api.ReqUserLogin.side_effect = lambda *args: simple_ctp_client.mdapi.OnRspUserLogin(login_field, None, 2, True)
    
    rsp_info = tdapi.CThostFtdcRspInfoField()
    rsp_info.ErrorID = 1
    rsp_info.ErrorMsg = "error"
    simple_ctp_client.tdapi.api.Init.side_effect = simple_ctp_client.tdapi.OnFrontConnected
    simple_ctp_client.tdapi.api.ReqAuthenticate.side_effect = lambda *args: simple_ctp_client.tdapi.OnRspAuthenticate(None, None, 1, True)
    simple_ctp_client.tdapi.api.ReqUserLogin.side_effect = lambda *args: simple_ctp_client.tdapi.OnRspUserLogin(None, rsp_info, 2, True)
    
    with pytest.raises(CtpException):
        simple_ctp_client.connect()
    assert simple_ctp_client.connected is False


def test_should_throw_exception_when_connect_give_td_authenticate_failed(simple_ctp_client: SimpleCtpClient):
    login_field = tdapi.CThostFtdcRspUserLoginField()
    simple_ctp_client.mdapi.api.Init.side_effect = simple_ctp_client.mdapi.OnFrontConnected
    simple_ctp_client.mdapi.api.ReqUserLogin.side_effect = lambda *args: simple_ctp_client.mdapi.OnRspUserLogin(login_field, None, 2, True)
    
    rsp_info = tdapi.CThostFtdcRspInfoField()
    rsp_info.ErrorID = 1
    rsp_info.ErrorMsg = "error"
    simple_ctp_client.tdapi.api.Init.side_effect = simple_ctp_client.tdapi.OnFrontConnected
    simple_ctp_client.tdapi.api.ReqAuthenticate.side_effect = lambda *args: simple_ctp_client.tdapi.OnRspAuthenticate(None, rsp_info, 1, True)
    simple_ctp_client.tdapi.api.ReqUserLogin.side_effect = lambda *args: simple_ctp_client.tdapi.OnRspUserLogin(login_field, None, 2, True)
    
    with pytest.raises(CtpException):
        simple_ctp_client.connect()
    assert simple_ctp_client.connected is False
