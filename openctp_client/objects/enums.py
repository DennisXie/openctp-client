from enum import Enum, auto


class CtpMethod(Enum):
    Connect = auto()
    Disconnect = auto()
    SubscribeMarketData = auto()
    OnRspUserLogin = auto()
    OnRspSubMarketData = auto()
    OnRtnDepthMarketData = auto()

    ReqSettlementInfoConfirm = auto()
    OnRspSettlementInfoConfirm = auto()
    OnRtnTrade = auto()
    OnRspQryInstrument = auto()
    ReqOrderInsert = auto()
    OnRspOrderInsert = auto()
    OnErrRtnOrderInsert = auto()
    
    @classmethod
    def nameOf(cls, name):
        return cls.__members__.get(name, None)
