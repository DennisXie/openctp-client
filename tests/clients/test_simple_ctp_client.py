import pytest
from pytest_mock import MockerFixture
from openctp_ctp import mdapi

from openctp_client.clients.simple_ctp_client import MdClient
from openctp_client.objects import *


@pytest.fixture
def spi_callback(mocker: MockerFixture):
    return mocker.stub(name="spi_callback")

@pytest.fixture
def config():
    conf = CtpConfig("tcp://test_address", "borker_id", "auth_code", "appi_id", "", "")
    return conf

@pytest.fixture
def client(config: CtpConfig, mocker: MockerFixture):
    mdapi = mocker.patch("openctp_client.clients.simple_ctp_client.mdapi")
    api = mocker.Mock(name="api")
    mdapi.CThostFtdcMdApi.CreateFtdcMdApi.return_value = api

    return MdClient(config)


def test_should_get_spi_callback_when_add_spi_callback_to_md_client(config: CtpConfig, spi_callback):
    client = MdClient(config)
    client.add_spi_callback(CtpMethod.OnOrderInsert, spi_callback)
    callbacks = client.get_spi_callback(CtpMethod.OnOrderInsert)
    assert len(callbacks) == 1
    assert callbacks[0] == spi_callback

def test_should_get_none_when_del_spi_callback_from_md_client(config: CtpConfig, spi_callback):
    client = MdClient(config)
    client.add_spi_callback(CtpMethod.OnOrderInsert, spi_callback)
    client.del_spi_callback(CtpMethod.OnOrderInsert, spi_callback)
    callbacks = client.get_spi_callback(CtpMethod.OnOrderInsert)
    assert len(callbacks) == 0

# The fixture seems called by the order of they are required by the test function
def test_should_call_Init_when_Connect(client):
    client.Connect()
    assert client.api.Init.called_once

def test_should_call_api_ReqUserLogin_when_OnFrontConnected(client):
    client.OnFrontConnected()
    assert client.api.ReqUserLogin.called_once

def test_should_call_callback_when_OnRspUserLogin(client, spi_callback):
    # given
    client.add_spi_callback(CtpMethod.OnRspUserLogin, spi_callback)
    pRspUserLogin = mdapi.CThostFtdcRspUserLoginField()
    pRspInfo = mdapi.CThostFtdcRspInfoField()
    # when
    client.OnRspUserLogin(pRspUserLogin, pRspInfo, 1, True)
    # should
    spi_callback.assert_called_once

def test_should_call_api_SubscribeMarketData_when_SubscribeMarketData(client):
    client.SubscribeMarketData(["rb2001", "ag2308"])
    assert client.api.SubscribeMarketData.called_once_with([b"rb2001", b"ag2308"])

def test_should_call_callback_when_OnRspSubMarketData(client, spi_callback):
    # given
    client.add_spi_callback(CtpMethod.OnRspSubMarketData, spi_callback)
    pSpecificInstrument = mdapi.CThostFtdcSpecificInstrumentField()
    pRspInfo = mdapi.CThostFtdcRspInfoField()
    # when
    client.OnRspSubMarketData(pSpecificInstrument, pRspInfo, 1, True)
    # should
    spi_callback.assert_called_once

def test_should_call_callback_when_OnRtnDepthMarketData(client, spi_callback):
    # given
    client.add_spi_callback(CtpMethod.OnRtnDepthMarketData, spi_callback)
    pDepthMarketData = mdapi.CThostFtdcDepthMarketDataField()
    # when
    client.OnRtnDepthMarketData(pDepthMarketData)
    # should
    spi_callback.assert_called_once
    