import pytest

from openctp_client.openctp import mdapi
from openctp_client.apis.md_api import MdAPI
from openctp_client.objects import *
from openctp_client.objects import CtpConfig


def test_should_get_spi_callback_when_set_spi_callback_to_md_api(config: CtpConfig, spi_callback):
    client = MdAPI(config)
    client.set_spi_callback(CtpMethod.OnRspOrderInsert, spi_callback)
    callback = client.get_spi_callback(CtpMethod.OnRspOrderInsert)
    assert callback == spi_callback


def test_should_get_none_when_del_spi_callback_from_md_api(config: CtpConfig, spi_callback):
    client = MdAPI(config)
    client.set_spi_callback(CtpMethod.OnRspOrderInsert, spi_callback)
    client.del_spi_callback(CtpMethod.OnRspOrderInsert)
    callback = client.get_spi_callback(CtpMethod.OnRspOrderInsert)
    assert callback is None


# The fixture seems called by the order of they are required by the test function
def test_should_call_Init_when_Connect(md_client: MdAPI):
    md_client.Connect()
    md_client.api.Init.assert_called_once()


def test_should_call_api_ReqUserLogin_when_OnFrontConnected(md_client):
    md_client.OnFrontConnected()
    md_client.api.ReqUserLogin.assert_called_once()


def test_should_call_callback_when_OnRspUserLogin(md_client, spi_callback):
    # given
    md_client.set_spi_callback(CtpMethod.OnRspUserLogin, spi_callback)
    pRspUserLogin = mdapi.CThostFtdcRspUserLoginField()
    pRspInfo = mdapi.CThostFtdcRspInfoField()
    # when
    md_client.OnRspUserLogin(pRspUserLogin, pRspInfo, 1, True)
    # should
    spi_callback.assert_called_once()


def test_should_call_api_SubscribeMarketData_when_SubscribeMarketData(md_client):
    md_client.SubscribeMarketData(["rb2001", "ag2308"])
    assert md_client.api.SubscribeMarketData.called_once_with([b"rb2001", b"ag2308"])


def test_should_call_callback_when_OnRspSubMarketData(md_client, spi_callback):
    # given
    md_client.set_spi_callback(CtpMethod.OnRspSubMarketData, spi_callback)
    pSpecificInstrument = mdapi.CThostFtdcSpecificInstrumentField()
    pRspInfo = mdapi.CThostFtdcRspInfoField()
    # when
    md_client.OnRspSubMarketData(pSpecificInstrument, pRspInfo, 1, True)
    # should
    spi_callback.assert_called_once()


def test_should_call_callback_when_OnRtnDepthMarketData(md_client, spi_callback):
    # given
    md_client.set_spi_callback(CtpMethod.OnRtnDepthMarketData, spi_callback)
    pDepthMarketData = mdapi.CThostFtdcDepthMarketDataField()
    # when
    md_client.OnRtnDepthMarketData(pDepthMarketData)
    # should
    spi_callback.assert_called_once()
   