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