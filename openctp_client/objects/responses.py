from pydantic import BaseModel, Field
from .enums import CtpMethod
from .fields import *


class CtpResponse(BaseModel):
    method: CtpMethod
    
    RspInfo: RspInfoField = Field(default_factory=RspInfoField)
    RequestID: Optional[int] = None
    IsLast: Optional[bool] = True
    
    @property
    def args(self) -> list[any]:
        return []


class RspUserLogin(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspUserLogin

    RspUserLogin: Optional[RspUserLoginField] = None
    
    @property
    def args(self) -> list[any]:
        return [self.RspUserLogin, self.RspInfo, self.RequestID, self.IsLast]


class RspSubMarketData(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspSubMarketData
    
    SpecificInstrument: Optional[SpecificInstrumentField] = None
    
    @property
    def args(self) -> list[any]:
        return [self.SpecificInstrument, self.RspInfo, self.RequestID, self.IsLast]


class RtnDepthMarketData(CtpResponse):
    method: CtpMethod = CtpMethod.OnRtnDepthMarketData
    
    DepthMarketData: Optional[DepthMarketDataField]
    
    @property
    def args(self) -> list[any]:
        return [self.DepthMarketData]


class RspQryInstrument(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspQryInstrument
    
    Instrument: Optional[InstrumentField] = None
    
    @property
    def args(self) -> list[any]:
        return [self.Instrument, self.RspInfo, self.RequestID, self.IsLast]


class RspOrderInsert(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspOrderInsert
    
    InputOrder: Optional[InputOrderField] = None
    
    @property
    def args(self) -> list[any]:
        return [self.InputOrder, self.RspInfo, self.RequestID, self.IsLast]


class ErrRtnOrderInsert(RspOrderInsert):
    method: CtpMethod = CtpMethod.OnErrRtnOrderInsert
    
    @property
    def args(self) -> list[any]:
        return [self.InputOrder, self.RspInfo]


class RtnOrder(CtpResponse):
    method: CtpMethod = CtpMethod.OnRtnOrder
    
    Order: Optional[OrderField] = None
    
    @property
    def args(self) -> list[any]:
        return [self.Order]


class RtnTrade(CtpResponse):
    method: CtpMethod = CtpMethod.OnRtnTrade
    
    Trade: Optional[TradeField] = None
    
    @property
    def args(self) -> list[any]:
        return [self.Trade]


class RspOrderAction(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspOrderAction
    
    InputOrderAction: Optional[InputOrderActionField] = None
    
    @property
    def args(self) -> list[any]:
        return [self.InputOrderAction, self.RspInfo, self.RequestID, self.IsLast]


class ErrRtnOrderAction(CtpResponse):
    method: CtpMethod = CtpMethod.OnErrRtnOrderAction
    
    OrderAction: Optional[OrderActionField] = None
    
    @property
    def args(self) -> list[any]:
        return [self.OrderAction, self.RspInfo]
