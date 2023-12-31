from typing import Any, Callable, Optional, Tuple
from ..openctp import mdapi

from ..objects.config import CtpConfig
from ..objects.enums import CtpMethod, Api
from ..objects.fields import *
from ..objects.responses import *


class MdAPI(mdapi.CThostFtdcMdSpi):
    
    def __init__(self, config: CtpConfig) -> None:
        super().__init__()
        self.config: CtpConfig = config
        self._request_count: int = 0
        self._callback: Callable[[CtpResponse], None] = self._default_callback
        self._spi_callback: dict[CtpMethod, Callable] = {}
        self._api: mdapi.CThostFtdcMdApi = mdapi.CThostFtdcMdApi.CreateFtdcMdApi(self.config.user_id)
        self._api.RegisterSpi(self)
        self._api.RegisterFront(self.config.md_addr)
    
    @property
    def api(self) -> mdapi.CThostFtdcMdApi:
        return self._api
    
    @property
    def request_id(self) -> int:
        self._request_count += 1
        return self._request_count
    
    @property
    def callback(self) -> Callable[[CtpResponse], None]:
        return self._callback
    
    @callback.setter
    def callback(self, callback: Callable[[CtpResponse], None]) -> None:
        self._callback = callback
    
    def log(self, *args, **kwargs) -> None:
        print(*args, **kwargs)
    
    def _default_callback(self, response: CtpResponse) -> None:
        if response.method in self._spi_callback:
            self._spi_callback[response.method](*response.args)
        else:
            # TODO: add warning
            self.log(f"no callback for {response.method.name()} found")
    
    def set_spi_callback(self, method: CtpMethod, callback: Callable) -> None:
        self._spi_callback[method] = callback
    
    def get_spi_callback(self, method: CtpMethod) -> Callable | None:
        return self._spi_callback.get(method)
    
    def del_spi_callback(self, method: CtpMethod) -> Callable | None:
        self._spi_callback.pop(method, None)
            
    def Connect(self) -> None:
        self.api.Init()
    
    def Disconnect(self) -> None:
        self.api.Release()
        self.api.Join()
    
    def OnFrontConnected(self):
        self._login()

    def OnFrontDisconnected(self, nReason):
        # TODO: add log
        pass
    
    def _login(self):
        req = mdapi.CThostFtdcReqUserLoginField()
        req.BrokerID = self.config.broker_id
        req.UserID = self.config.user_id
        req.Password = self.config.password
        self.api.ReqUserLogin(req, self.request_id)

    def OnRspUserLogin(self, pRspUserLogin: mdapi.CThostFtdcRspUserLoginField, pRspInfo: mdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """called when login responding"""
        rsp = RspUserLogin(
            RspUserLogin=RspUserLoginField.from_ctp_object(pRspUserLogin),
            RspInfo=RspInfoField.from_ctp_object(pRspInfo),
            RequestID=nRequestID,
            IsLast=bIsLast
        )
        rsp.source = Api.Md
            
        if pRspInfo is not None:
            self.log(f"login rsp info, ErrorID: {pRspInfo.ErrorID}, ErrorMsg: {pRspInfo.ErrorMsg}")
            
        self.callback(rsp)
   
    def SubscribeMarketData(self, instrument_ids: list[str]) -> Tuple[int, int]:
        instrument_ids = list(map(lambda i: i.encode(), instrument_ids))
        request_id = self.request_id
        ret = self.api.SubscribeMarketData(instrument_ids, request_id)
        return (request_id, ret)
    
    def OnRspSubMarketData(self, pSpecificInstrument: mdapi.CThostFtdcSpecificInstrumentField, pRspInfo: mdapi.CThostFtdcRspInfoField, nRequestID, bIsLast):
        rsp = RspSubMarketData(
            SpecificInstrument=SpecificInstrumentField.from_ctp_object(pSpecificInstrument),
            RspInfo=RspInfoField.from_ctp_object(pRspInfo),
            RequestID=nRequestID,
            IsLast=bIsLast
        )
        self.callback(rsp)

    def OnRtnDepthMarketData(self, pDepthMarketData: mdapi.CThostFtdcDepthMarketDataField):
        rsp = RtnDepthMarketData(DepthMarketData=DepthMarketDataField.from_ctp_object(pDepthMarketData))
        self.callback(rsp)

            
    # 理论上用户回调和SPI回调函数重名没有问题，但是这样真的好吗？
    # def __setattr__(self, __name: str, __value: Any) -> None:
    #     method = CtpMethod.nameOf(__name)
    #     if method:
    #         self._call_map[method] = __value
    #     else:
    #         return super().__setattr__(__name, __value)
    
    # def __getattribute__(self, __name: str) -> Any:
    #     method = CtpMethod.nameOf(__name)
    #     if method and method in self._call_map:
    #         return self._call_map[method]
    #     else:
    #         return super().__getattribute__(__name)
    
    # def __delattr__(self, __name: str) -> None:
    #     method = CtpMethod.nameOf(__name)
    #     if method and method in self._call_map:
    #         del self._call_map[method]
    #     else:
    #         return super().__delattr__(__name)
