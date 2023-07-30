from enum import Enum, auto


class CtpMethod(Enum):
    # Used by td and md
    Connect = auto()
    Disconnect = auto()
    
    # Used by md
    SubscribeMarketData = auto()
    OnRspUserLogin = auto()
    OnRspSubMarketData = auto()
    OnRtnDepthMarketData = auto()

    # Used by td
    ReqSettlementInfoConfirm = auto()
    OnRspSettlementInfoConfirm = auto()
    ReqQryInstrument = auto()
    OnRspQryInstrument = auto()
    ReqOrderInsert = auto()
    OnRspOrderInsert = auto()
    OnRtnOrder = auto()
    OnErrRtnOrderInsert = auto()
    OnRtnTrade = auto()
    ReqOrderAction = auto()
    OnRspOrderAction = auto()
    OnErrRtnOrderAction = auto()
    ReqQryTradingAccount = auto()
    OnRspQryTradingAccount = auto()
    ReqQryInvestorPosition = auto()
    OnRspQryInvestorPosition = auto()
    ReqQryTrade = auto()
    OnRspQryTrade = auto()
    ReqQryOrder = auto()
    OnRspQryOrder = auto()
    
    @classmethod
    def nameOf(cls, name):
        return cls.__members__.get(name, None)
