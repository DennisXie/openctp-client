import pytest
from pytest_mock import MockerFixture
from openctp_ctp import tdapi

from openctp_client.clients.td_client import TdClient
from openctp_client.objects import *


@pytest.fixture
def td_client(config: CtpConfig, mocker: MockerFixture):
    tdapi = mocker.patch("openctp_client.clients.td_client.tdapi")
    api = mocker.Mock(name="api")
    tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi.return_value = api
    return TdClient(config)


def test_should_create_TdClient(config: CtpConfig):
    td_client = TdClient(config)
    assert td_client is not None
    assert td_client.config is config
    assert td_client.request_id == 1
    assert td_client.api is not None


def test_should_have_default_callback(td_client: TdClient):
    assert td_client.callback is not None


def test_should_set_callback(td_client: TdClient, spi_callback):
    td_client.callback = spi_callback
    assert td_client.callback is spi_callback


def test_should_get_spi_callback_when_set_spi_callback_to_td_client(config: CtpConfig, spi_callback):
    td_client = TdClient(config)
    td_client.set_spi_callback(CtpMethod.OnOrderInsert, spi_callback)
    callback = td_client.get_spi_callback(CtpMethod.OnOrderInsert)
    assert callback is spi_callback


def test_should_get_none_when_spi_callback_not_set(config: CtpConfig, spi_callback):
    td_client = TdClient(config)
    td_client.set_spi_callback(CtpMethod.OnRtnTrade, spi_callback)
    callback = td_client.get_spi_callback(CtpMethod.OnOrderInsert)
    assert callback is None


def test_should_get_none_when_del_spi_callback_from_md_client(config: CtpConfig, spi_callback):
    td_client = TdClient(config)
    td_client.set_spi_callback(CtpMethod.OnOrderInsert, spi_callback)
    deleted_callback = td_client.del_spi_callback(CtpMethod.OnOrderInsert)
    callback = td_client.get_spi_callback(CtpMethod.OnOrderInsert)
    assert deleted_callback is spi_callback
    assert callback is None


def test_should_call_Init_when_Connect(td_client: TdClient):
    td_client.Connect()
    td_client.api.Init.assert_called_once_with()


def test_should_call_api_ReqAuthenticate_when_OnFrontConnected(td_client: TdClient):
    td_client.OnFrontConnected()
    td_client.api.ReqAuthenticate.assert_called_once()


def test_should_call_api_ReqUserLogin_when_OnRspAuthenticate_success(td_client: TdClient):
    # given
    authenticate = tdapi.CThostFtdcRspAuthenticateField()
    rsp_info = tdapi.CThostFtdcRspInfoField()
    rsp_info.ErrorID = 0
    rsp_info.ErrorMsg = ""
    
    # when
    td_client.OnRspAuthenticate(authenticate, rsp_info, 1, True)
    
    # then
    td_client.api.ReqUserLogin.assert_called_once()


def test_should_xx_when_OnRspAuthenticate_fail(td_client: TdClient):
    # given
    authenticate = tdapi.CThostFtdcRspAuthenticateField()
    rsp_info = tdapi.CThostFtdcRspInfoField()
    rsp_info.ErrorID = 1
    rsp_info.ErrorMsg = ""
    
    # when
    td_client.OnRspAuthenticate(authenticate, rsp_info, 1, True)
    
    # then
    td_client.api.ReqUserLogin.assert_not_called()
    # TODO: assert authentication failed notification is sent


def test_should_call_callback_when_OnRspUserLogin(td_client: TdClient, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspUserLogin, spi_callback)
    pRspUserLogin = tdapi.CThostFtdcRspUserLoginField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspUserLogin(pRspUserLogin, pRspInfo, 2, True)
    # should
    spi_callback.assert_called_once()