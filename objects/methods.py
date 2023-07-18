from enum import Enum, auto, IntFlag


class CtpMethod(Enum):
    Connect = auto(IntFlag)
    Disconnect = auto(IntFlag)
    SubscribeMarketData = auto(IntFlag)
    OnRspSubMarketData = auto(IntFlag)
    OnRtnDepthMarketData = auto(IntFlag)

    ReqSettlementInfoConfirm = auto(IntFlag)
    OnRspSettlementInfoConfirm = auto(IntFlag)
    ReqOrderInsert = auto(IntFlag)
    OnOrderInsert = auto(IntFlag)
    OnErrRtnOrderInsert = auto(IntFlag)
    OnRtnTrade = auto(IntFlag)
