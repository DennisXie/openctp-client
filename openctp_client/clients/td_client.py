from typing import Callable, Tuple
from openctp_ctp import tdapi

from ..objects.config import CtpConfig
from ..objects.enums import CtpMethod
from ..objects.fields import *
from ..objects.responses import *


class TdClient(tdapi.CThostFtdcTraderSpi):
    
    def __init__(self, config: CtpConfig) -> None:
        super().__init__()
        self.config = config
        self._request_count = 0
        self._callback = self._default_callback
        self._spi_callback: dict[CtpMethod, Callable] = {}
        self._api: tdapi.CThostFtdcTraderApi = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi(self.config.user_id)
        self._api.RegisterSpi(self)
        self._api.RegisterFront(self.config.addr)
    
    @property
    def request_id(self) -> int:
        self._request_count += 1
        return self._request_count
    
    @property
    def api(self) -> tdapi.CThostFtdcTraderApi:
        return self._api
    
    @property
    def callback(self) -> Callable:
        return self._callback
    
    @callback.setter
    def callback(self, callback: Callable) -> None:
        self._callback = callback
    
    def log(self, *args, **kwargs) -> None:
        print(*args, **kwargs)
    
    def _default_callback(self, response: CtpResponse) -> None:
        if response.method in self._spi_callback:
            self._spi_callback[response.method](*response.args)
        else:
            # TODO: add warning
            self.log(f"no callback for {response.method.name()} found")

    
    def set_spi_callback(self, method: CtpMethod, callback: Callable):
        self._spi_callback[method] = callback
    
    def get_spi_callback(self, method: CtpMethod) -> Callable | None:
        return self._spi_callback.get(method)
    
    def del_spi_callback(self, method: CtpMethod) -> Callable | None:
        return self._spi_callback.pop(method, None)
    
    def Connect(self) -> None:
        self.api.Init()
    
    def Disconnect(self) -> None:
        self.api.Release()
        self.api.Join()
    
    def OnFrontConnected(self) -> None:
        req = tdapi.CThostFtdcReqAuthenticateField()
        req.BrokerID = self.config.broker_id
        req.UserID = self.config.user_id
        req.AuthCode = self.config.auth_code
        req.AppID = self.config.app_id
        self._api.ReqAuthenticate(req, self.request_id)
    
    def OnRspAuthenticate(self, pRspAuthenticateField, pRspInfo, nRequestID, bIsLast):
        if pRspInfo is None or pRspInfo.ErrorID == 0:
            self._login()
        else:
            self._authenticate_failed(pRspInfo)
    
    def _login(self) -> None:
        req = tdapi.CThostFtdcReqUserLoginField()
        req.BrokerID = self.config.broker_id
        req.UserID = self.config.user_id
        req.Password = self.config.password
        self._api.ReqUserLogin(req, self.request_id)
    
    def _authenticate_failed(self, pRspInfo) -> None:
        # TODO: how to notify upstream that authentication failed?
        pass
    
    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        """called when login responding"""
        rsp = RspUserLogin(
            RspUserLogin=RspUserLoginField.from_ctp_object(pRspUserLogin),
            RspInfo=RspInfoField.from_ctp_object(pRspInfo),
            RequestID=nRequestID,
            IsLast=bIsLast
        )
            
        if pRspInfo is not None:
            self.log(f"login rsp info, ErrorID: {pRspInfo.ErrorID}, ErrorMsg: {pRspInfo.ErrorMsg}")
            
        self.callback(rsp)
    
    def ReqQryInstrument(self, qry_instrument: QryInstrumentField, req_id: int | None = None) -> int:
        # TODO: use exception to throw the api error, and return the request_id
        req = qry_instrument.ctp_object()
        req_id = req_id or self.request_id
        return self._api.ReqQryInstrument(req, req_id)
    
    def OnRspQryInstrument(self, pInstrument: tdapi.CThostFtdcInstrumentField, pRspInfo, nRequestID, bIsLast):
        rsp = RspQryInstrument(
            RspQryInstrument=InstrumentField.from_ctp_object(pInstrument),
            RspInfo=RspInfoField.from_ctp_object(pRspInfo),
            RequestID=nRequestID,
            IsLast=bIsLast
        )
        self.callback(rsp)
    
    def ReqOrderInsert(self, input_order: InputOrderField, req_id: int | None = None) -> None:
        req = input_order.ctp_object()
        req_id = req_id or self.request_id
        return self._api.ReqOrderInsert(req, req_id)
        
    def OnRspOrderInsert(self, pInputOrder: tdapi.CThostFtdcInputOrderField, pRspInfo, nRequestID, bIsLast):
        """Error raised by the CTP"""
        rsp = RspOrderInsert(
            RspOrderInsert=InputOrderField.from_ctp_object(pInputOrder),
            RspInfo=RspInfoField.from_ctp_object(pRspInfo),
            RequestID=nRequestID,
            IsLast=bIsLast
        )
        self.callback(rsp)
    
    def OnErrRtnOrderInsert(self, pInputOrder: tdapi.CThostFtdcInputOrderField, pRspInfo):
        """Error raised by the exchange"""
        rsp = ErrRtnOrderInsert(
            ErrRtnOrderInsert=InputOrderField.from_ctp_object(pInputOrder),
            RspInfo=RspInfoField.from_ctp_object(pRspInfo),
        )
        self.callback(rsp)
    
    def OnRtnOrder(self, pOrder: tdapi.CThostFtdcOrderField):
        """Success order insert or order action"""
        rsp = RtnOrder(
            RtnOrder=OrderField.from_ctp_object(pOrder),
        )
        self.callback(rsp)
    
    def OnRtnTrade(self, pTrade: tdapi.CThostFtdcTradeField):
        rsp = RtnTrade(
            RtnTrade=TradeField.from_ctp_object(pTrade),
        )
        self.callback(rsp)
    
    def ReqOrderAction(self, input_order_action: InputOrderActionField, req_id: int | None = None) -> None:
        req = input_order_action.ctp_object()
        req_id = req_id or self.request_id
        return self._api.ReqOrderAction(req, req_id)
    
    def OnRspOrderAction(self, pInputOrderAction: tdapi.CThostFtdcInputOrderActionField, pRspInfo, nRequestID, bIsLast):
        """Error raised by the CTP"""
        rsp = RspOrderAction(
            RspOrderAction=InputOrderActionField.from_ctp_object(pInputOrderAction),
            RspInfo=RspInfoField.from_ctp_object(pRspInfo),
            RequestID=nRequestID,
            IsLast=bIsLast
        )
        self.callback(rsp)
    
    def OnErrRtnOrderAction(self, pInputOrderAction: tdapi.CThostFtdcInputOrderActionField, pRspInfo):
        """Error raised by the exchange"""
        rsp = ErrRtnOrderAction(
            ErrRtnOrderAction=InputOrderActionField.from_ctp_object(pInputOrderAction),
            RspInfo=RspInfoField.from_ctp_object(pRspInfo),
        )
        self.callback(rsp)
