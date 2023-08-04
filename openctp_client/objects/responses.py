from typing import Any
from pydantic import BaseModel, Field
from .enums import CtpMethod, Api
from .fields import *


class CtpResponse(BaseModel):
    method: CtpMethod
    
    RspInfo: RspInfoField = Field(default_factory=RspInfoField)
    RequestID: Optional[int] = None
    IsLast: Optional[bool] = True
    
    @property
    def args(self) -> list[Any]:
        return []
    
    @property
    def ok(self) -> bool:
        return self.RspInfo.ok


class RspAuthenticate(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspAuthenticate
    
    @property
    def args(self) -> list[Any]:
        return [self.RspInfo, self.RequestID, self.IsLast]


class RspUserLogin(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspUserLogin
    _source: Api

    RspUserLogin: Optional[RspUserLoginField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.RspUserLogin, self.RspInfo, self.RequestID, self.IsLast]
    
    @property
    def source(self) -> Api:
        return self._source
    
    @source.setter
    def source(self, src: Api) -> None:
        self._source = src


class RspSubMarketData(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspSubMarketData
    
    SpecificInstrument: Optional[SpecificInstrumentField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.SpecificInstrument, self.RspInfo, self.RequestID, self.IsLast]


class RtnDepthMarketData(CtpResponse):
    method: CtpMethod = CtpMethod.OnRtnDepthMarketData
    
    DepthMarketData: Optional[DepthMarketDataField]
    
    @property
    def args(self) -> list[Any]:
        return [self.DepthMarketData]


class RspQrySettlementInfo(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspQrySettlementInfo
    
    SettlementInfo: Optional[SettlementInfoField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.SettlementInfo, self.RspInfo, self.RequestID, self.IsLast]


class RspQrySettlementInfoConfirm(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspQrySettlementInfoConfirm
    
    SettlementInfoConfirm: Optional[SettlementInfoConfirmField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.SettlementInfoConfirm, self.RspInfo, self.RequestID, self.IsLast]


class RspQryInstrument(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspQryInstrument
    
    Instrument: Optional[InstrumentField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.Instrument, self.RspInfo, self.RequestID, self.IsLast]


class RspOrderInsert(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspOrderInsert
    
    InputOrder: Optional[InputOrderField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.InputOrder, self.RspInfo, self.RequestID, self.IsLast]


class ErrRtnOrderInsert(RspOrderInsert):
    method: CtpMethod = CtpMethod.OnErrRtnOrderInsert
    
    @property
    def args(self) -> list[Any]:
        return [self.InputOrder, self.RspInfo]


class RtnOrder(CtpResponse):
    method: CtpMethod = CtpMethod.OnRtnOrder
    
    Order: Optional[OrderField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.Order]


class RtnTrade(CtpResponse):
    method: CtpMethod = CtpMethod.OnRtnTrade
    
    Trade: Optional[TradeField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.Trade]


class RspOrderAction(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspOrderAction
    
    InputOrderAction: Optional[InputOrderActionField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.InputOrderAction, self.RspInfo, self.RequestID, self.IsLast]


class ErrRtnOrderAction(CtpResponse):
    method: CtpMethod = CtpMethod.OnErrRtnOrderAction
    
    OrderAction: Optional[OrderActionField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.OrderAction, self.RspInfo]


class RspQryInvestorPosition(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspQryInvestorPosition
    
    InvestorPosition: Optional[InvestorPositionField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.InvestorPosition, self.RspInfo, self.RequestID, self.IsLast]


class RspQryTradingAccount(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspQryTradingAccount
    
    TradingAccount: Optional[TradingAccountField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.TradingAccount, self.RspInfo, self.RequestID, self.IsLast]


class RspQryTrade(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspQryTrade
    
    Trade: Optional[TradeField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.Trade, self.RspInfo, self.RequestID, self.IsLast]


class RspQryOrder(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspQryOrder
    
    Order: Optional[OrderField] = None
    
    @property
    def args(self) -> list[Any]:
        return [self.Order, self.RspInfo, self.RequestID, self.IsLast]
