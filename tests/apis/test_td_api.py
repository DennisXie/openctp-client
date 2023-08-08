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
    td_client.api.Init.assert_called_once()


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
    authenticate.AppID = "1111"
    rsp_info = tdapi.CThostFtdcRspInfoField()
    rsp_info.ErrorID = 1
    rsp_info.ErrorMsg = ""
    
    # when
    td_client.OnRspAuthenticate(authenticate, rsp_info, 1, True)
    
    # then
    authenticate_field = RspAuthenticateField.from_ctp_object(authenticate)
    rsp_info_field = RspInfoField.from_ctp_object(rsp_info)
    spi_callback.assert_called_once_with(authenticate_field, rsp_info_field, 1, True)


def test_should_call_callback_when_OnRspUserLogin(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspUserLogin, spi_callback)
    pRspUserLogin = tdapi.CThostFtdcRspUserLoginField()
    pRspUserLogin.BrokerID = "9999"
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspUserLogin(pRspUserLogin, pRspInfo, 2, True)
    # should
    user_login_field = RspUserLoginField.from_ctp_object(pRspUserLogin)
    rsp_info_field = RspInfoField.from_ctp_object(pRspInfo)
    spi_callback.assert_called_once_with(user_login_field, rsp_info_field, 2, True)


def test_should_call_api_ReqQrySettlementInfo_when_ReqQrySettlementInfo(td_client: TdAPI):
    req = QrySettlementInfoField()
    td_client.ReqQrySettlementInfo(req)
    td_client.api.ReqQrySettlementInfo.assert_called_once()


def test_should_call_callback_when_OnRspQrySettlementInfo(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQrySettlementInfo, spi_callback)
    pSettlementInfo = tdapi.CThostFtdcSettlementInfoField()
    pSettlementInfo.AccountID = "1234"
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQrySettlementInfo(pSettlementInfo, pRspInfo, 2, True)
    # should
    settlement_info = SettlementInfoField.from_ctp_object(pSettlementInfo)
    rsp_info = RspInfoField.from_ctp_object(pRspInfo)
    spi_callback.assert_called_once_with(settlement_info, rsp_info, 2, True)


def test_should_call_api_ReqQrySettlementInfoConfirm_when_ReqQrySettlementInfoConfirm(td_client: TdAPI):
    req = SettlementInfoConfirmField()
    td_client.ReqQrySettlementInfoConfirm(req)
    td_client.api.ReqQrySettlementInfoConfirm.assert_called_once()


def test_should_call_callback_when_OnRspQrySettlementInfoConfirm(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQrySettlementInfoConfirm, spi_callback)
    pSettlementInfoConfirm = tdapi.CThostFtdcSettlementInfoConfirmField()
    pSettlementInfoConfirm.BrokerID = "9999"
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQrySettlementInfoConfirm(pSettlementInfoConfirm, pRspInfo, 2, True)
    # should
    settlement_info_confirm = SettlementInfoConfirmField.from_ctp_object(pSettlementInfoConfirm)
    rsp_info = RspInfoField.from_ctp_object(pRspInfo)
    spi_callback.assert_called_once_with(settlement_info_confirm, rsp_info, 2, True)


def test_should_call_api_ReqQryInstrument_when_ReqQryInstrument(td_client: TdAPI):
    req = QryInstrumentField()
    td_client.ReqQryInstrument(req)
    td_client.api.ReqQryInstrument.assert_called_once()


def test_should_call_callback_when_OnRspQryInstrument(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQryInstrument, spi_callback)
    pInstrument = tdapi.CThostFtdcInstrumentField()
    pInstrument.InstrumentID = "ag2312"
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQryInstrument(pInstrument, pRspInfo, 2, True)
    # should
    instrument = InstrumentField.from_ctp_object(pInstrument)
    rsp_info = RspInfoField.from_ctp_object(pRspInfo)
    spi_callback.assert_called_once_with(instrument, rsp_info, 2, True)


def test_should_call_api_ReqOrderInsert_when_ReqOrderInsert(td_client: TdAPI):
    req = InputOrderField()
    td_client.ReqOrderInsert(req)
    td_client.api.ReqOrderInsert.assert_called_once()


def test_should_call_callback_when_OnRspOrderInsert(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspOrderInsert, spi_callback)
    pInputOrder = tdapi.CThostFtdcInputOrderField()
    pInputOrder.AccountID = "123"
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspOrderInsert(pInputOrder, pRspInfo, 2, True)
    # should
    input_order = InputOrderField.from_ctp_object(pInputOrder)
    rsp_info = RspInfoField.from_ctp_object(pRspInfo)
    spi_callback.assert_called_once_with(input_order, rsp_info, 2, True)


def test_should_call_callback_when_OnErrRtnOrderInsert(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnErrRtnOrderInsert, spi_callback)
    pInputOrder = tdapi.CThostFtdcInputOrderField()
    pInputOrder.AccountID = "123"
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnErrRtnOrderInsert(pInputOrder, pRspInfo)
    # should
    input_order = InputOrderField.from_ctp_object(pInputOrder)
    rsp_info = RspInfoField.from_ctp_object(pRspInfo)
    spi_callback.assert_called_once_with(input_order, rsp_info)


def test_should_call_callback_when_OnRtnOrder(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRtnOrder, spi_callback)
    pOrder = tdapi.CThostFtdcOrderField()
    pOrder.AccountID = "123"
    # when
    td_client.OnRtnOrder(pOrder)
    # should
    order = OrderField.from_ctp_object(pOrder)
    spi_callback.assert_called_once_with(order)


def test_should_call_callback_when_OnRtnTrade(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRtnTrade, spi_callback)
    pTrade = tdapi.CThostFtdcTradeField()
    pTrade.BrokerID = "9999"
    # when
    td_client.OnRtnTrade(pTrade)
    # should
    trade = TradeField.from_ctp_object(pTrade)
    spi_callback.assert_called_once_with(trade)


def test_should_call_api_ReqOrderAction_when_ReqOrderAction(td_client: TdAPI):
    req = InputOrderActionField()
    td_client.ReqOrderAction(req)
    td_client.api.ReqOrderAction.assert_called_once()


def test_should_call_callback_when_OnRspOrderAction(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspOrderAction, spi_callback)
    pInputOrderAction = tdapi.CThostFtdcInputOrderActionField()
    pInputOrderAction.BrokerID = "9999"
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspOrderAction(pInputOrderAction, pRspInfo, 2, True)
    # should
    input_order_action = InputOrderActionField.from_ctp_object(pInputOrderAction)
    rsp_info = RspInfoField.from_ctp_object(pRspInfo)
    spi_callback.assert_called_once_with(input_order_action, rsp_info, 2, True)
    

def test_should_call_callback_when_OnErrRtnOrderAction(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnErrRtnOrderAction, spi_callback)
    pOrderAction = tdapi.CThostFtdcOrderActionField()
    pOrderAction.BrokerID = "9999"
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnErrRtnOrderAction(pOrderAction, pRspInfo)
    # should
    order_action = OrderActionField.from_ctp_object(pOrderAction)
    rsp_info = RspInfoField.from_ctp_object(pRspInfo)
    spi_callback.assert_called_once_with(order_action, rsp_info)


def test_should_call_api_ReqQryTradingAccount_when_ReqQryTradingAccount(td_client: TdAPI):
    req = QryTradingAccountField()
    td_client.ReqQryTradingAccount(req)
    td_client.api.ReqQryTradingAccount.assert_called_once()


def test_should_call_callback_when_OnRspQryTradingAccount(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQryTradingAccount, spi_callback)
    pTradingAccount = tdapi.CThostFtdcTradingAccountField()
    pTradingAccount.AccountID = "123"
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQryTradingAccount(pTradingAccount, pRspInfo, 2, True)
    # should
    trading_account = TradingAccountField.from_ctp_object(pTradingAccount)
    rsp_info = RspInfoField.from_ctp_object(pRspInfo)
    spi_callback.assert_called_once_with(trading_account, rsp_info, 2, True)


def test_should_call_api_ReqQryInvestorPosition_when_ReqQryInvestorPosition(td_client: TdAPI):
    req = QryInvestorPositionField()
    td_client.ReqQryInvestorPosition(req)
    td_client.api.ReqQryInvestorPosition.assert_called_once()


def test_should_call_callback_when_OnRspQryInvestorPosition(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQryInvestorPosition, spi_callback)
    pInvestorPosition = tdapi.CThostFtdcInvestorPositionField()
    pInvestorPosition.BrokerID = "9999"
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQryInvestorPosition(pInvestorPosition, pRspInfo, 2, True)
    # should
    investor_position = InvestorPositionField.from_ctp_object(pInvestorPosition)
    rsp_info = RspInfoField.from_ctp_object(pRspInfo)
    spi_callback.assert_called_once_with(investor_position, rsp_info, 2, True)


def test_should_call_api_ReqQryOrder_when_ReqQryOrder(td_client: TdAPI):
    req = QryOrderField()
    td_client.ReqQryOrder(req)
    td_client.api.ReqQryOrder.assert_called_once()


def test_should_call_callback_when_OnRspQryOrder(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQryOrder, spi_callback)
    pOrder = tdapi.CThostFtdcOrderField()
    pOrder.BrokerID = "9999"
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQryOrder(pOrder, pRspInfo, 2, True)
    # should
    order = OrderField.from_ctp_object(pOrder)
    rsp_info = RspInfoField.from_ctp_object(pRspInfo)
    spi_callback.assert_called_once_with(order, rsp_info, 2, True)


def test_should_call_api_ReqQryTrade_when_ReqQryTrade(td_client: TdAPI):
    req = QryTradeField()
    td_client.ReqQryTrade(req)
    td_client.api.ReqQryTrade.assert_called_once()


def test_should_call_callback_when_OnRspQryTrade(td_client: TdAPI, spi_callback):
    # given
    td_client.set_spi_callback(CtpMethod.OnRspQryTrade, spi_callback)
    pTrade = tdapi.CThostFtdcTradeField()
    pTrade.BrokerID = "9999"
    pRspInfo = tdapi.CThostFtdcRspInfoField()
    # when
    td_client.OnRspQryTrade(pTrade, pRspInfo, 2, True)
    # should
    trade = TradeField.from_ctp_object(pTrade)
    rsp_info = RspInfoField.from_ctp_object(pRspInfo)
    spi_callback.assert_called_once_with(trade, rsp_info, 2, True)
