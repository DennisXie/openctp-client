import pytest
from pytest_mock import MockerFixture

from openctp_client.clients import SimpleCtpClient, SimpleCtpClientEvent
from openctp_client.exceptions import CtpException
from openctp_client.objects import *
from openctp_client.objects.responses import *
from openctp_client.openctp import tdapi


@pytest.fixture
def mock_td_md(mocker: MockerFixture):
    tdapi = mocker.patch("openctp_client.apis.td_api.tdapi")
    tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi.return_value = mocker.Mock(name="tdapi")
    mdapi = mocker.patch("openctp_client.apis.md_api.mdapi")
    mdapi.CThostFtdcMdApi.CreateFtdcMdApi.return_value = mocker.Mock(name="mdapi")


@pytest.fixture
def simple_ctp_client(config: CtpConfig, mock_td_md, mocker):
    client = SimpleCtpClient(config)
    client._start_process = mocker.Mock()
    client._stop_process = mocker.Mock()
    client._produce_rsp = mocker.Mock()
    client._produce_rsp.side_effect = lambda rsp: client._process_rsp(rsp)
    client.tdapi.callback = client._produce_rsp
    client.mdapi.callback = client._produce_rsp
    return client


def test_should_create_simple_ctp_client(config: CtpConfig):
    client = SimpleCtpClient(config)
    assert client is not None
    assert client.tdapi is not None
    assert client.mdapi is not None


def test_should_have_callback_when_on_event(simple_ctp_client: SimpleCtpClient, mocker):
    fn = mocker.Mock()
    simple_ctp_client.on_event(SimpleCtpClientEvent.on_account, fn)
    assert fn in simple_ctp_client._event_callback[SimpleCtpClientEvent.on_account]


def test_should_del_callback_when_off_event(simple_ctp_client: SimpleCtpClient, mocker):
    fn = mocker.Mock()
    simple_ctp_client.on_event(SimpleCtpClientEvent.on_account, fn)
    simple_ctp_client.off_event(SimpleCtpClientEvent.on_account, fn)
    assert fn not in simple_ctp_client._event_callback[SimpleCtpClientEvent.on_account]


def test_should_consume_when_produce_rsp(config: CtpConfig, mocker):
    # given
    client = SimpleCtpClient(config)
    client._process_rsp = mocker.Mock()
    rsp = CtpResponse(method=CtpMethod.OnErrRtnOrderAction)
    client._produce_rsp(rsp)
    client._stop_process()
    # when
    client._consume_rsp()
    # should
    client._process_rsp.assert_called_once_with(rsp)


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


# @pytest.mark.skip
def test_should_call_callback_when_OnRtnDepthMarketData(simple_ctp_client: SimpleCtpClient, mocker):
    # given
    market_data = DepthMarketDataField(TradingDay="20231212", AskPrice1=19.22)
    rtn_depth_market_data = RtnDepthMarketData(DepthMarketData=market_data)
    fn = mocker.Mock()
    simple_ctp_client.on_event(SimpleCtpClientEvent.on_tick, fn)
    # when
    simple_ctp_client._produce_rsp(rtn_depth_market_data)
    # then
    fn.assert_called_once_with(market_data)
