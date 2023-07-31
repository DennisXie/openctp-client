from enum import Enum, auto


class Api(Enum):
    Td = auto()
    Md = auto()


class CtpMethod(Enum):
    # Used by td and md
    Connect = auto()
    Disconnect = auto()
    OnRspUserLogin = auto()
    
    # Used by md
    SubscribeMarketData = auto()
    OnRspSubMarketData = auto()
    OnRtnDepthMarketData = auto()

    # Used by td
    OnRspAuthenticate = auto()
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
