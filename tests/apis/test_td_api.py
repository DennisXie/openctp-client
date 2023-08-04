import pytest
from pytest_mock import MockerFixture

from openctp_client.openctp import tdapi
from openctp_client.apis.td_api import TdAPI
from openctp_client.objects import *


def test_should_create_TdClient(config: CtpConfig):
    td_client = TdAPI(config)
    assert td_client is not None
    assert td_client.config is config
    assert td_client.request_id == 1
    assert td_client.api is not None


def test_should_have_default_callback(td_client: TdAPI):
    assert td_client.callback is not None


def test_should_set_callback(td_client: TdAPI, spi_callback):
    td_client.callback = spi_callback
    assert td_client.callback is spi_callback


def test_should_get_spi_callback_when_set_spi_callback_to_td_api(config: CtpConfig, spi_callback):
    td_client = TdAPI(config)
    td_client.set_spi_callback(CtpMethod.OnRspOrderInsert, spi_callback)
    callback = td_client.get_spi_callback(CtpMethod.OnRspOrderInsert)
    assert callback is spi_callback


def test_should_get_none_when_spi_callback_not_set(config: CtpConfig, spi_callback):
    td_client = TdAPI(config)
    td_client.set_spi_callback(CtpMethod.OnRtnTrade, spi_callback)
    callback = td_client.get_spi_callback(CtpMethod.OnRspOrderInsert)
    assert callback is None


def test_should_get_none_when_del_spi_callback_from_td_api(config: CtpConfig, spi_callback):
    td_client = TdAPI(config)
    td_client.set_spi_callback(CtpMethod.OnRspOrderInsert, spi_callback)
    deleted_callback = td_client.del_spi_callback(CtpMethod.OnRspOrderInsert)
    callback = td_client.get_spi_callback(CtpMethod.OnRspOrderInsert)
    assert deleted_callback is spi_callback
    assert callback is None


def test_should_call_Init_when_Connect(td_client: TdAPI):
    td_client.Connect()
    td_client.api.Init.assert_called_once_with()


def test_should_call_api_ReqAuthenticate_when_OnFrontConnected(td_client: TdAPI):
    td_client.OnFrontConnected()
    td_client.api.ReqAuthenticate.assert_called_once()


def test_should_call_api_ReqUserLogin_when_OnRspAuthenticate_success(td_client: TdAPI):
    # given
    authenticate = tdapi.CThostFtdcRspAuthenticateField()
    rsp_info = tdapi.CThostFtdcRspInfoField()
    rsp_info.ErrorID = 0
    rsp_info.ErrorMsg = ""
    
    # when
    td_client.OnRspAuthenticate(authenticate, rsp_info, 1, True)
    
    # then
    td_client.api.ReqUserLogin.assert_called_once()


def test_should_call_callback_when_OnRspAuthenticate_fail(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspAuthenticate, spi_callback)
    authenticate = tdapi.CThostFtdcRspAuthenticateField()
    rsp_info = tdapi.CThostFtdcRspInfoField()
    rsp_info.ErrorID = 1
    rsp_info.ErrorMsg = ""
    
    # when
    td_client.OnRspAuthenticate(authenticate, rsp_info, 1, True)
    
    # then
    spi_callback.assert_called_once()


def test_should_call_callback_when_OnRspUserLogin(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspUserLogin, spi_callback)
    pRspUserLogin = tdapi.CThostFtdcRspUserLoginField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspUserLogin(pRspUserLogin, pRspInfo, 2, True)
    # should
    spi_callback.assert_called_once()


def test_should_call_api_ReqQrySettlementInfo_when_ReqQrySettlementInfo(td_client: TdAPI):
    req = QrySettlementInfoField()
    td_client.ReqQrySettlementInfo(req)
    td_client.api.ReqQrySettlementInfo.assert_called_once()


def test_should_call_callback_when_OnRspQrySettlementInfo(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQrySettlementInfo, spi_callback)
    pSettlementInfo = tdapi.CThostFtdcSettlementInfoField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQrySettlementInfo(pSettlementInfo, pRspInfo, 2, True)
    # should
    spi_callback.assert_called_once()


def test_should_call_api_ReqQrySettlementInfoConfirm_when_ReqQrySettlementInfoConfirm(td_client: TdAPI):
    req = SettlementInfoConfirmField()
    td_client.ReqQrySettlementInfoConfirm(req)
    td_client.api.ReqQrySettlementInfoConfirm.assert_called_once()


def test_should_call_callback_when_OnRspQrySettlementInfoConfirm(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQrySettlementInfoConfirm, spi_callback)
    pSettlementInfoConfirm = tdapi.CThostFtdcSettlementInfoConfirmField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQrySettlementInfoConfirm(pSettlementInfoConfirm, pRspInfo, 2, True)
    # should
    spi_callback.assert_called_once()


def test_should_call_api_ReqQryInstrument_when_ReqQryInstrument(td_client: TdAPI):
    req = QryInstrumentField()
    td_client.ReqQryInstrument(req)
    td_client.api.ReqQryInstrument.assert_called_once()


def test_should_call_callback_when_OnRspQryInstrument(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQryInstrument, spi_callback)
    pInstrument = tdapi.CThostFtdcInstrumentField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQryInstrument(pInstrument, pRspInfo, 2, True)
    # should
    spi_callback.assert_called_once()


def test_should_call_api_ReqOrderInsert_when_ReqOrderInsert(td_client: TdAPI):
    req = InputOrderField()
    td_client.ReqOrderInsert(req)
    td_client.api.ReqOrderInsert.assert_called_once()


def test_should_call_callback_when_OnRspOrderInsert(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspOrderInsert, spi_callback)
    pInputOrder = tdapi.CThostFtdcInputOrderField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspOrderInsert(pInputOrder, pRspInfo, 2, True)
    # should
    spi_callback.assert_called_once()


def test_should_call_callback_when_OnErrRtnOrderInsert(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnErrRtnOrderInsert, spi_callback)
    pInputOrder = tdapi.CThostFtdcInputOrderField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnErrRtnOrderInsert(pInputOrder, pRspInfo)
    # should
    spi_callback.assert_called_once()


def test_should_call_callback_when_OnRtnOrder(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRtnOrder, spi_callback)
    pOrder = tdapi.CThostFtdcOrderField()
    # when
    td_client.OnRtnOrder(pOrder)
    # should
    spi_callback.assert_called_once()


def test_should_call_callback_when_OnRtnTrade(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRtnTrade, spi_callback)
    pTrade = tdapi.CThostFtdcTradeField()
    # when
    td_client.OnRtnTrade(pTrade)
    # should
    spi_callback.assert_called_once()


def test_should_call_api_ReqOrderAction_when_ReqOrderAction(td_client: TdAPI):
    req = InputOrderActionField()
    td_client.ReqOrderAction(req)
    td_client.api.ReqOrderAction.assert_called_once()


def test_should_call_callback_when_OnRspOrderAction(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspOrderAction, spi_callback)
    pInputOrderAction = tdapi.CThostFtdcInputOrderActionField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspOrderAction(pInputOrderAction, pRspInfo, 2, True)
    # should
    spi_callback.assert_called_once()
    

def test_should_call_callback_when_OnErrRtnOrderAction(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnErrRtnOrderAction, spi_callback)
    pOrderAction = tdapi.CThostFtdcOrderActionField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnErrRtnOrderAction(pOrderAction, pRspInfo)
    # should
    spi_callback.assert_called_once()


def test_should_call_api_ReqQryTradingAccount_when_ReqQryTradingAccount(td_client: TdAPI):
    req = QryTradingAccountField()
    td_client.ReqQryTradingAccount(req)
    td_client.api.ReqQryTradingAccount.assert_called_once()


def test_should_call_callback_when_OnRspQryTradingAccount(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQryTradingAccount, spi_callback)
    pTradingAccount = tdapi.CThostFtdcTradingAccountField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQryTradingAccount(pTradingAccount, pRspInfo, 2, True)
    # should
    spi_callback.assert_called_once()


def test_should_call_api_ReqQryInvestorPosition_when_ReqQryInvestorPosition(td_client: TdAPI):
    req = QryInvestorPositionField()
    td_client.ReqQryInvestorPosition(req)
    td_client.api.ReqQryInvestorPosition.assert_called_once()


def test_should_call_callback_when_OnRspQryInvestorPosition(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQryInvestorPosition, spi_callback)
    pInvestorPosition = tdapi.CThostFtdcInvestorPositionField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQryInvestorPosition(pInvestorPosition, pRspInfo, 2, True)
    # should
    spi_callback.assert_called_once()


def test_should_call_api_ReqQryOrder_when_ReqQryOrder(td_client: TdAPI):
    req = QryOrderField()
    td_client.ReqQryOrder(req)
    td_client.api.ReqQryOrder.assert_called_once()


def test_should_call_callback_when_OnRspQryOrder(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQryOrder, spi_callback)
    pOrder = tdapi.CThostFtdcOrderField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQryOrder(pOrder, pRspInfo, 2, True)
    # should
    spi_callback.assert_called_once()


def test_should_call_api_ReqQryTrade_when_ReqQryTrade(td_client: TdAPI):
    req = QryTradeField()
    td_client.ReqQryTrade(req)
    td_client.api.ReqQryTrade.assert_called_once()


def test_should_call_callback_when_OnRspQryTrade(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQryTrade, spi_callback)
    pTrade = tdapi.CThostFtdcTradeField()
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQryTrade(pTrade, pRspInfo, 2, True)
    # should
    spi_callback.assert_called_once()
