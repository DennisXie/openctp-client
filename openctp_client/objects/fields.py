from typing import ClassVar, Optional, TypeVar
from pydantic import BaseModel, Field, constr, ConfigDict
from openctp_ctp import tdapi


class CtpField(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    _ctp_type_: ClassVar[callable] = None

    def ctp_object(self) -> any:
        obj = self._ctp_type_()
        for key, value in self.model_dump().items():
            if value is not None:
                setattr(obj, key, value)
        return obj
    
    @classmethod
    def from_ctp_object(cls: 'CtpField', obj: any) -> 'CtpField':
        return cls.model_validate(obj) if obj else None


class ReqUserLoginField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcReqUserLoginField
    
    TradingDay: Optional[constr(max_length=9)] = Field(None, description='交易日')
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    Password: Optional[constr(max_length=41)] = Field(None, description='密码')
    UserProductInfo: Optional[constr(max_length=11)] = Field(
        None, description='用户端产品信息'
    )
    InterfaceProductInfo: Optional[constr(max_length=11)] = Field(
        None, description='接口端产品信息'
    )
    ProtocolInfo: Optional[constr(max_length=11)] = Field(None, description='协议信息')
    MacAddress: Optional[constr(max_length=21)] = Field(None, description='Mac地址')
    OneTimePassword: Optional[constr(max_length=41)] = Field(None, description='动态密码')
    LoginRemark: Optional[constr(max_length=36)] = Field(None, description='登录备注')
    ClientIPPort: Optional[int] = Field(None, description='终端IP端口')
    ClientIPAddress: Optional[constr(max_length=33)] = Field(None, description='终端IP地址')


class RspUserLoginField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcRspUserLoginField
    
    TradingDay: Optional[constr(max_length=9)] = Field(None, description='交易日')
    LoginTime: Optional[constr(max_length=9)] = Field(None, description='登录成功时间')
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    SystemName: Optional[constr(max_length=41)] = Field(None, description='交易系统名称')
    FrontID: Optional[int] = Field(None, description='前置编号')
    SessionID: Optional[int] = Field(None, description='会话编号')
    MaxOrderRef: Optional[constr(max_length=13)] = Field(None, description='最大报单引用')
    SHFETime: Optional[constr(max_length=9)] = Field(None, description='上期所时间')
    DCETime: Optional[constr(max_length=9)] = Field(None, description='大商所时间')
    CZCETime: Optional[constr(max_length=9)] = Field(None, description='郑商所时间')
    FFEXTime: Optional[constr(max_length=9)] = Field(None, description='中金所时间')
    INETime: Optional[constr(max_length=9)] = Field(None, description='能源中心时间')
    SysVersion: Optional[constr(max_length=41)] = Field(None, description='后台版本信息')


class UserLogoutField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcUserLogoutField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')


class ReqAuthenticateField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcReqAuthenticateField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    UserProductInfo: Optional[constr(max_length=11)] = Field(
        None, description='用户端产品信息'
    )
    AuthCode: Optional[constr(max_length=17)] = Field(None, description='认证码')
    AppID: Optional[constr(max_length=33)] = Field(None, description='App代码')


class RspAuthenticateField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcRspAuthenticateField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    UserProductInfo: Optional[constr(max_length=11)] = Field(
        None, description='用户端产品信息'
    )
    AppID: Optional[constr(max_length=33)] = Field(None, description='App代码')
    AppType: Optional[constr(max_length=1)] = Field(None, description='App类型')


class AuthenticationInfoField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcAuthenticationInfoField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    UserProductInfo: Optional[constr(max_length=11)] = Field(
        None, description='用户端产品信息'
    )
    AuthInfo: Optional[constr(max_length=129)] = Field(None, description='认证信息')
    IsResult: Optional[int] = Field(None, description='是否为认证结果')
    AppID: Optional[constr(max_length=33)] = Field(None, description='App代码')
    AppType: Optional[constr(max_length=1)] = Field(None, description='App类型')
    ClientIPAddress: Optional[constr(max_length=33)] = Field(None, description='终端IP地址')


class RspInfoField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcRspInfoField
    
    ErrorID: Optional[int] = Field(default=0, description='错误代码')
    ErrorMsg: Optional[constr(max_length=81)] = Field(default="", description='错误信息')
    
    @classmethod
    def from_ctp_object(cls: CtpField, obj: any) -> CtpField:
        return cls.model_validate(obj) if obj else cls()
    
    @property
    def ok(self) -> bool:
        return self.ErrorID == 0


class QrySettlementInfoField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcQrySettlementInfoField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    TradingDay: Optional[constr(max_length=9)] = Field(None, description='交易日')
    AccountID: Optional[constr(max_length=13)] = Field(None, description='投资者帐号')
    CurrencyID: Optional[constr(max_length=4)] = Field(None, description='币种代码')


class SettlementInfoField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcSettlementInfoField
    
    TradingDay: Optional[constr(max_length=9)] = Field(None, description='交易日')
    SettlementID: Optional[int] = Field(None, description='结算编号')
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    SequenceNo: Optional[int] = Field(None, description='序号')
    Content: Optional[constr(max_length=501)] = Field(None, description='消息正文')
    AccountID: Optional[constr(max_length=13)] = Field(None, description='投资者帐号')
    CurrencyID: Optional[constr(max_length=4)] = Field(None, description='币种代码')


class QrySettlementInfoConfirmField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcQrySettlementInfoConfirmField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    AccountID: Optional[constr(max_length=13)] = Field(None, description='投资者帐号')
    CurrencyID: Optional[constr(max_length=4)] = Field(None, description='币种代码')

   
class SettlementInfoConfirmField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcSettlementInfoConfirmField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    ConfirmDate: Optional[constr(max_length=9)] = Field(None, description='确认日期')
    ConfirmTime: Optional[constr(max_length=9)] = Field(None, description='确认时间')
    SettlementID: Optional[int] = Field(None, description='结算编号')
    AccountID: Optional[constr(max_length=13)] = Field(None, description='投资者帐号')
    CurrencyID: Optional[constr(max_length=4)] = Field(None, description='币种代码')


    
class ExchangeField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcExchangeField
    
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    ExchangeName: Optional[constr(max_length=61)] = Field(None, description='交易所名称')
    ExchangeProperty: Optional[constr(max_length=1)] = Field(None, description='交易所属性')


class ProductField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcProductField
    
    ProductName: Optional[constr(max_length=21)] = Field(None, description='产品名称')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    ProductClass: Optional[constr(max_length=1)] = Field(None, description='产品类型')
    VolumeMultiple: Optional[int] = Field(None, description='合约数量乘数')
    PriceTick: Optional[float] = Field(None, description='最小变动价位')
    MaxMarketOrderVolume: Optional[int] = Field(None, description='市价单最大下单量')
    MinMarketOrderVolume: Optional[int] = Field(None, description='市价单最小下单量')
    MaxLimitOrderVolume: Optional[int] = Field(None, description='限价单最大下单量')
    MinLimitOrderVolume: Optional[int] = Field(None, description='限价单最小下单量')
    PositionType: Optional[constr(max_length=1)] = Field(None, description='持仓类型')
    PositionDateType: Optional[constr(max_length=1)] = Field(None, description='持仓日期类型')
    CloseDealType: Optional[constr(max_length=1)] = Field(None, description='平仓处理类型')
    TradeCurrencyID: Optional[constr(max_length=4)] = Field(None, description='交易币种类型')
    MortgageFundUseRange: Optional[constr(max_length=1)] = Field(
        None, description='质押资金可用范围'
    )
    UnderlyingMultiple: Optional[float] = Field(None, description='合约基础商品乘数')
    ProductID: Optional[constr(max_length=81)] = Field(None, description='产品代码')
    ExchangeProductID: Optional[constr(max_length=81)] = Field(
        None, description='交易所产品代码'
    )
    OpenLimitControlLevel: Optional[constr(max_length=1)] = Field(
        None, description='开仓量限制粒度'
    )
    OrderFreqControlLevel: Optional[constr(max_length=1)] = Field(
        None, description='报单频率控制粒度'
    )


class QryInstrumentField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcQryInstrumentField
    
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
    ExchangeInstID: Optional[constr(max_length=81)] = Field(
        None, description='合约在交易所的代码'
    )
    ProductID: Optional[constr(max_length=81)] = Field(None, description='产品代码')


class InstrumentField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcInstrumentField
    
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    InstrumentName: Optional[constr(max_length=21)] = Field(None, description='合约名称')
    ProductClass: Optional[constr(max_length=1)] = Field(None, description='产品类型')
    DeliveryYear: Optional[int] = Field(None, description='交割年份')
    DeliveryMonth: Optional[int] = Field(None, description='交割月')
    MaxMarketOrderVolume: Optional[int] = Field(None, description='市价单最大下单量')
    MinMarketOrderVolume: Optional[int] = Field(None, description='市价单最小下单量')
    MaxLimitOrderVolume: Optional[int] = Field(None, description='限价单最大下单量')
    MinLimitOrderVolume: Optional[int] = Field(None, description='限价单最小下单量')
    VolumeMultiple: Optional[int] = Field(None, description='合约数量乘数')
    PriceTick: Optional[float] = Field(None, description='最小变动价位')
    CreateDate: Optional[constr(max_length=9)] = Field(None, description='创建日')
    OpenDate: Optional[constr(max_length=9)] = Field(None, description='上市日')
    ExpireDate: Optional[constr(max_length=9)] = Field(None, description='到期日')
    StartDelivDate: Optional[constr(max_length=9)] = Field(None, description='开始交割日')
    EndDelivDate: Optional[constr(max_length=9)] = Field(None, description='结束交割日')
    InstLifePhase: Optional[constr(max_length=1)] = Field(None, description='合约生命周期状态')
    IsTrading: Optional[int] = Field(None, description='当前是否交易')
    PositionType: Optional[constr(max_length=1)] = Field(None, description='持仓类型')
    PositionDateType: Optional[constr(max_length=1)] = Field(None, description='持仓日期类型')
    LongMarginRatio: Optional[float] = Field(None, description='多头保证金率')
    ShortMarginRatio: Optional[float] = Field(None, description='空头保证金率')
    MaxMarginSideAlgorithm: Optional[constr(max_length=1)] = Field(
        None, description='是否使用大额单边保证金算法'
    )
    StrikePrice: Optional[float] = Field(None, description='执行价')
    OptionsType: Optional[constr(max_length=1)] = Field(None, description='期权类型')
    UnderlyingMultiple: Optional[float] = Field(None, description='合约基础商品乘数')
    CombinationType: Optional[constr(max_length=1)] = Field(None, description='组合类型')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
    ExchangeInstID: Optional[constr(max_length=81)] = Field(
        None, description='合约在交易所的代码'
    )
    ProductID: Optional[constr(max_length=81)] = Field(None, description='产品代码')
    UnderlyingInstrID: Optional[constr(max_length=81)] = Field(
        None, description='基础商品代码'
    )


class SpecificInstrumentField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcSpecificInstrumentField
    
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
    
    
class DepthMarketDataField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcDepthMarketDataField
    
    TradingDay: Optional[constr(max_length=9)] = Field(None, description='交易日')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    LastPrice: Optional[float] = Field(None, description='最新价')
    PreSettlementPrice: Optional[float] = Field(None, description='上次结算价')
    PreClosePrice: Optional[float] = Field(None, description='昨收盘')
    PreOpenInterest: Optional[float] = Field(None, description='昨持仓量')
    OpenPrice: Optional[float] = Field(None, description='今开盘')
    HighestPrice: Optional[float] = Field(None, description='最高价')
    LowestPrice: Optional[float] = Field(None, description='最低价')
    Volume: Optional[int] = Field(None, description='数量')
    Turnover: Optional[float] = Field(None, description='成交金额')
    OpenInterest: Optional[float] = Field(None, description='持仓量')
    ClosePrice: Optional[float] = Field(None, description='今收盘')
    SettlementPrice: Optional[float] = Field(None, description='本次结算价')
    UpperLimitPrice: Optional[float] = Field(None, description='涨停板价')
    LowerLimitPrice: Optional[float] = Field(None, description='跌停板价')
    PreDelta: Optional[float] = Field(None, description='昨虚实度')
    CurrDelta: Optional[float] = Field(None, description='今虚实度')
    UpdateTime: Optional[constr(max_length=9)] = Field(None, description='最后修改时间')
    UpdateMillisec: Optional[int] = Field(None, description='最后修改毫秒')
    BidPrice1: Optional[float] = Field(None, description='申买价一')
    BidVolume1: Optional[int] = Field(None, description='申买量一')
    AskPrice1: Optional[float] = Field(None, description='申卖价一')
    AskVolume1: Optional[int] = Field(None, description='申卖量一')
    BidPrice2: Optional[float] = Field(None, description='申买价二')
    BidVolume2: Optional[int] = Field(None, description='申买量二')
    AskPrice2: Optional[float] = Field(None, description='申卖价二')
    AskVolume2: Optional[int] = Field(None, description='申卖量二')
    BidPrice3: Optional[float] = Field(None, description='申买价三')
    BidVolume3: Optional[int] = Field(None, description='申买量三')
    AskPrice3: Optional[float] = Field(None, description='申卖价三')
    AskVolume3: Optional[int] = Field(None, description='申卖量三')
    BidPrice4: Optional[float] = Field(None, description='申买价四')
    BidVolume4: Optional[int] = Field(None, description='申买量四')
    AskPrice4: Optional[float] = Field(None, description='申卖价四')
    AskVolume4: Optional[int] = Field(None, description='申卖量四')
    BidPrice5: Optional[float] = Field(None, description='申买价五')
    BidVolume5: Optional[int] = Field(None, description='申买量五')
    AskPrice5: Optional[float] = Field(None, description='申卖价五')
    AskVolume5: Optional[int] = Field(None, description='申卖量五')
    AveragePrice: Optional[float] = Field(None, description='当日均价')
    ActionDay: Optional[constr(max_length=9)] = Field(None, description='业务日期')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
    ExchangeInstID: Optional[constr(max_length=81)] = Field(
        None, description='合约在交易所的代码'
    )
    BandingUpperPrice: Optional[float] = Field(None, description='上带价')
    BandingLowerPrice: Optional[float] = Field(None, description='下带价')


class InputOrderField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcInputOrderField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    OrderRef: Optional[constr(max_length=13)] = Field(None, description='报单引用')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    OrderPriceType: Optional[constr(max_length=1)] = Field(None, description='报单价格条件')
    Direction: Optional[constr(max_length=1)] = Field(None, description='买卖方向')
    CombOffsetFlag: Optional[constr(max_length=5)] = Field(None, description='组合开平标志')
    CombHedgeFlag: Optional[constr(max_length=5)] = Field(None, description='组合投机套保标志')
    LimitPrice: Optional[float] = Field(None, description='价格')
    VolumeTotalOriginal: Optional[int] = Field(None, description='数量')
    TimeCondition: Optional[constr(max_length=1)] = Field(None, description='有效期类型')
    GTDDate: Optional[constr(max_length=9)] = Field(None, description='GTD日期')
    VolumeCondition: Optional[constr(max_length=1)] = Field(None, description='成交量类型')
    MinVolume: Optional[int] = Field(None, description='最小成交量')
    ContingentCondition: Optional[constr(max_length=1)] = Field(
        None, description='触发条件'
    )
    StopPrice: Optional[float] = Field(None, description='止损价')
    ForceCloseReason: Optional[constr(max_length=1)] = Field(None, description='强平原因')
    IsAutoSuspend: Optional[int] = Field(None, description='自动挂起标志')
    BusinessUnit: Optional[constr(max_length=21)] = Field(None, description='业务单元')
    RequestID: Optional[int] = Field(None, description='请求编号')
    UserForceClose: Optional[int] = Field(None, description='用户强评标志')
    IsSwapOrder: Optional[int] = Field(None, description='互换单标志')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    InvestUnitID: Optional[constr(max_length=17)] = Field(None, description='投资单元代码')
    AccountID: Optional[constr(max_length=13)] = Field(None, description='资金账号')
    CurrencyID: Optional[constr(max_length=4)] = Field(None, description='币种代码')
    ClientID: Optional[constr(max_length=11)] = Field(None, description='交易编码')
    MacAddress: Optional[constr(max_length=21)] = Field(None, description='Mac地址')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
    IPAddress: Optional[constr(max_length=33)] = Field(None, description='IP地址')


class OrderField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcOrderField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    OrderRef: Optional[constr(max_length=13)] = Field(None, description='报单引用')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    OrderPriceType: Optional[constr(max_length=1)] = Field(None, description='报单价格条件')
    Direction: Optional[constr(max_length=1)] = Field(None, description='买卖方向')
    CombOffsetFlag: Optional[constr(max_length=5)] = Field(None, description='组合开平标志')
    CombHedgeFlag: Optional[constr(max_length=5)] = Field(None, description='组合投机套保标志')
    LimitPrice: Optional[float] = Field(None, description='价格')
    VolumeTotalOriginal: Optional[int] = Field(None, description='数量')
    TimeCondition: Optional[constr(max_length=1)] = Field(None, description='有效期类型')
    GTDDate: Optional[constr(max_length=9)] = Field(None, description='GTD日期')
    VolumeCondition: Optional[constr(max_length=1)] = Field(None, description='成交量类型')
    MinVolume: Optional[int] = Field(None, description='最小成交量')
    ContingentCondition: Optional[constr(max_length=1)] = Field(
        None, description='触发条件'
    )
    StopPrice: Optional[float] = Field(None, description='止损价')
    ForceCloseReason: Optional[constr(max_length=1)] = Field(None, description='强平原因')
    IsAutoSuspend: Optional[int] = Field(None, description='自动挂起标志')
    BusinessUnit: Optional[constr(max_length=21)] = Field(None, description='业务单元')
    RequestID: Optional[int] = Field(None, description='请求编号')
    OrderLocalID: Optional[constr(max_length=13)] = Field(None, description='本地报单编号')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    ParticipantID: Optional[constr(max_length=11)] = Field(None, description='会员代码')
    ClientID: Optional[constr(max_length=11)] = Field(None, description='客户代码')
    TraderID: Optional[constr(max_length=21)] = Field(None, description='交易所交易员代码')
    InstallID: Optional[int] = Field(None, description='安装编号')
    OrderSubmitStatus: Optional[constr(max_length=1)] = Field(
        None, description='报单提交状态'
    )
    NotifySequence: Optional[int] = Field(None, description='报单提示序号')
    TradingDay: Optional[constr(max_length=9)] = Field(None, description='交易日')
    SettlementID: Optional[int] = Field(None, description='结算编号')
    OrderSysID: Optional[constr(max_length=21)] = Field(None, description='报单编号')
    OrderSource: Optional[constr(max_length=1)] = Field(None, description='报单来源')
    OrderStatus: Optional[constr(max_length=1)] = Field(None, description='报单状态')
    OrderType: Optional[constr(max_length=1)] = Field(None, description='报单类型')
    VolumeTraded: Optional[int] = Field(None, description='今成交数量')
    VolumeTotal: Optional[int] = Field(None, description='剩余数量')
    InsertDate: Optional[constr(max_length=9)] = Field(None, description='报单日期')
    InsertTime: Optional[constr(max_length=9)] = Field(None, description='委托时间')
    ActiveTime: Optional[constr(max_length=9)] = Field(None, description='激活时间')
    SuspendTime: Optional[constr(max_length=9)] = Field(None, description='挂起时间')
    UpdateTime: Optional[constr(max_length=9)] = Field(None, description='最后修改时间')
    CancelTime: Optional[constr(max_length=9)] = Field(None, description='撤销时间')
    ActiveTraderID: Optional[constr(max_length=21)] = Field(
        None, description='最后修改交易所交易员代码'
    )
    ClearingPartID: Optional[constr(max_length=11)] = Field(None, description='结算会员编号')
    SequenceNo: Optional[int] = Field(None, description='序号')
    FrontID: Optional[int] = Field(None, description='前置编号')
    SessionID: Optional[int] = Field(None, description='会话编号')
    UserProductInfo: Optional[constr(max_length=11)] = Field(
        None, description='用户端产品信息'
    )
    StatusMsg: Optional[constr(max_length=81)] = Field(None, description='状态信息')
    UserForceClose: Optional[int] = Field(None, description='用户强评标志')
    ActiveUserID: Optional[constr(max_length=16)] = Field(None, description='操作用户代码')
    BrokerOrderSeq: Optional[int] = Field(None, description='经纪公司报单编号')
    RelativeOrderSysID: Optional[constr(max_length=21)] = Field(
        None, description='相关报单'
    )
    ZCETotalTradedVolume: Optional[int] = Field(None, description='郑商所成交数量')
    IsSwapOrder: Optional[int] = Field(None, description='互换单标志')
    BranchID: Optional[constr(max_length=9)] = Field(None, description='营业部编号')
    InvestUnitID: Optional[constr(max_length=17)] = Field(None, description='投资单元代码')
    AccountID: Optional[constr(max_length=13)] = Field(None, description='资金账号')
    CurrencyID: Optional[constr(max_length=4)] = Field(None, description='币种代码')
    MacAddress: Optional[constr(max_length=21)] = Field(None, description='Mac地址')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
    ExchangeInstID: Optional[constr(max_length=81)] = Field(
        None, description='合约在交易所的代码'
    )
    IPAddress: Optional[constr(max_length=33)] = Field(None, description='IP地址')


class TradeField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcTradeField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    OrderRef: Optional[constr(max_length=13)] = Field(None, description='报单引用')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    TradeID: Optional[constr(max_length=21)] = Field(None, description='成交编号')
    Direction: Optional[constr(max_length=1)] = Field(None, description='买卖方向')
    OrderSysID: Optional[constr(max_length=21)] = Field(None, description='报单编号')
    ParticipantID: Optional[constr(max_length=11)] = Field(None, description='会员代码')
    ClientID: Optional[constr(max_length=11)] = Field(None, description='客户代码')
    TradingRole: Optional[constr(max_length=1)] = Field(None, description='交易角色')
    OffsetFlag: Optional[constr(max_length=1)] = Field(None, description='开平标志')
    HedgeFlag: Optional[constr(max_length=1)] = Field(None, description='投机套保标志')
    Price: Optional[float] = Field(None, description='价格')
    Volume: Optional[int] = Field(None, description='数量')
    TradeDate: Optional[constr(max_length=9)] = Field(None, description='成交时期')
    TradeTime: Optional[constr(max_length=9)] = Field(None, description='成交时间')
    TradeType: Optional[constr(max_length=1)] = Field(None, description='成交类型')
    PriceSource: Optional[constr(max_length=1)] = Field(None, description='成交价来源')
    TraderID: Optional[constr(max_length=21)] = Field(None, description='交易所交易员代码')
    OrderLocalID: Optional[constr(max_length=13)] = Field(None, description='本地报单编号')
    ClearingPartID: Optional[constr(max_length=11)] = Field(None, description='结算会员编号')
    BusinessUnit: Optional[constr(max_length=21)] = Field(None, description='业务单元')
    SequenceNo: Optional[int] = Field(None, description='序号')
    TradingDay: Optional[constr(max_length=9)] = Field(None, description='交易日')
    SettlementID: Optional[int] = Field(None, description='结算编号')
    BrokerOrderSeq: Optional[int] = Field(None, description='经纪公司报单编号')
    TradeSource: Optional[constr(max_length=1)] = Field(None, description='成交来源')
    InvestUnitID: Optional[constr(max_length=17)] = Field(None, description='投资单元代码')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
    ExchangeInstID: Optional[constr(max_length=81)] = Field(
        None, description='合约在交易所的代码'
    )


class InputOrderActionField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcInputOrderActionField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    OrderActionRef: Optional[int] = Field(None, description='报单操作引用')
    OrderRef: Optional[constr(max_length=13)] = Field(None, description='报单引用')
    RequestID: Optional[int] = Field(None, description='请求编号')
    FrontID: Optional[int] = Field(None, description='前置编号')
    SessionID: Optional[int] = Field(None, description='会话编号')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    OrderSysID: Optional[constr(max_length=21)] = Field(None, description='报单编号')
    ActionFlag: Optional[constr(max_length=1)] = Field(None, description='操作标志')
    LimitPrice: Optional[float] = Field(None, description='价格')
    VolumeChange: Optional[int] = Field(None, description='数量变化')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    InvestUnitID: Optional[constr(max_length=17)] = Field(None, description='投资单元代码')
    MacAddress: Optional[constr(max_length=21)] = Field(None, description='Mac地址')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
    IPAddress: Optional[constr(max_length=33)] = Field(None, description='IP地址')


class OrderActionField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcOrderActionField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    OrderActionRef: Optional[int] = Field(None, description='报单操作引用')
    OrderRef: Optional[constr(max_length=13)] = Field(None, description='报单引用')
    RequestID: Optional[int] = Field(None, description='请求编号')
    FrontID: Optional[int] = Field(None, description='前置编号')
    SessionID: Optional[int] = Field(None, description='会话编号')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    OrderSysID: Optional[constr(max_length=21)] = Field(None, description='报单编号')
    ActionFlag: Optional[constr(max_length=1)] = Field(None, description='操作标志')
    LimitPrice: Optional[float] = Field(None, description='价格')
    VolumeChange: Optional[int] = Field(None, description='数量变化')
    ActionDate: Optional[constr(max_length=9)] = Field(None, description='操作日期')
    ActionTime: Optional[constr(max_length=9)] = Field(None, description='操作时间')
    TraderID: Optional[constr(max_length=21)] = Field(None, description='交易所交易员代码')
    InstallID: Optional[int] = Field(None, description='安装编号')
    OrderLocalID: Optional[constr(max_length=13)] = Field(None, description='本地报单编号')
    ActionLocalID: Optional[constr(max_length=13)] = Field(None, description='操作本地编号')
    ParticipantID: Optional[constr(max_length=11)] = Field(None, description='会员代码')
    ClientID: Optional[constr(max_length=11)] = Field(None, description='客户代码')
    BusinessUnit: Optional[constr(max_length=21)] = Field(None, description='业务单元')
    OrderActionStatus: Optional[constr(max_length=1)] = Field(
        None, description='报单操作状态'
    )
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    StatusMsg: Optional[constr(max_length=81)] = Field(None, description='状态信息')
    BranchID: Optional[constr(max_length=9)] = Field(None, description='营业部编号')
    InvestUnitID: Optional[constr(max_length=17)] = Field(None, description='投资单元代码')
    MacAddress: Optional[constr(max_length=21)] = Field(None, description='Mac地址')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
    IPAddress: Optional[constr(max_length=33)] = Field(None, description='IP地址')


class QryOrderField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcQryOrderField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    OrderSysID: Optional[constr(max_length=21)] = Field(None, description='报单编号')
    InsertTimeStart: Optional[constr(max_length=9)] = Field(None, description='开始时间')
    InsertTimeEnd: Optional[constr(max_length=9)] = Field(None, description='结束时间')
    InvestUnitID: Optional[constr(max_length=17)] = Field(None, description='投资单元代码')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')


class QryTradeField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcQryTradeField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    TradeID: Optional[constr(max_length=21)] = Field(None, description='成交编号')
    TradeTimeStart: Optional[constr(max_length=9)] = Field(None, description='开始时间')
    TradeTimeEnd: Optional[constr(max_length=9)] = Field(None, description='结束时间')
    InvestUnitID: Optional[constr(max_length=17)] = Field(None, description='投资单元代码')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')


class QryInvestorPositionField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcQryInvestorPositionField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    InvestUnitID: Optional[constr(max_length=17)] = Field(None, description='投资单元代码')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')


class QryTradingAccountField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcQryTradingAccountField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    CurrencyID: Optional[constr(max_length=4)] = Field(None, description='币种代码')
    BizType: Optional[constr(max_length=1)] = Field(None, description='业务类型')
    AccountID: Optional[constr(max_length=13)] = Field(None, description='投资者帐号')


class QryInvestorField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcQryInvestorField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')


class TradingAccountField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcTradingAccountField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    AccountID: Optional[constr(max_length=13)] = Field(None, description='投资者帐号')
    PreMortgage: Optional[float] = Field(None, description='上次质押金额')
    PreCredit: Optional[float] = Field(None, description='上次信用额度')
    PreDeposit: Optional[float] = Field(None, description='上次存款额')
    PreBalance: Optional[float] = Field(None, description='上次结算准备金')
    PreMargin: Optional[float] = Field(None, description='上次占用的保证金')
    InterestBase: Optional[float] = Field(None, description='利息基数')
    Interest: Optional[float] = Field(None, description='利息收入')
    Deposit: Optional[float] = Field(None, description='入金金额')
    Withdraw: Optional[float] = Field(None, description='出金金额')
    FrozenMargin: Optional[float] = Field(None, description='冻结的保证金')
    FrozenCash: Optional[float] = Field(None, description='冻结的资金')
    FrozenCommission: Optional[float] = Field(None, description='冻结的手续费')
    CurrMargin: Optional[float] = Field(None, description='当前保证金总额')
    CashIn: Optional[float] = Field(None, description='资金差额')
    Commission: Optional[float] = Field(None, description='手续费')
    CloseProfit: Optional[float] = Field(None, description='平仓盈亏')
    PositionProfit: Optional[float] = Field(None, description='持仓盈亏')
    Balance: Optional[float] = Field(None, description='期货结算准备金')
    Available: Optional[float] = Field(None, description='可用资金')
    WithdrawQuota: Optional[float] = Field(None, description='可取资金')
    Reserve: Optional[float] = Field(None, description='基本准备金')
    TradingDay: Optional[constr(max_length=9)] = Field(None, description='交易日')
    SettlementID: Optional[int] = Field(None, description='结算编号')
    Credit: Optional[float] = Field(None, description='信用额度')
    Mortgage: Optional[float] = Field(None, description='质押金额')
    ExchangeMargin: Optional[float] = Field(None, description='交易所保证金')
    DeliveryMargin: Optional[float] = Field(None, description='投资者交割保证金')
    ExchangeDeliveryMargin: Optional[float] = Field(None, description='交易所交割保证金')
    ReserveBalance: Optional[float] = Field(None, description='保底期货结算准备金')
    CurrencyID: Optional[constr(max_length=4)] = Field(None, description='币种代码')
    PreFundMortgageIn: Optional[float] = Field(None, description='上次货币质入金额')
    PreFundMortgageOut: Optional[float] = Field(None, description='上次货币质出金额')
    FundMortgageIn: Optional[float] = Field(None, description='货币质入金额')
    FundMortgageOut: Optional[float] = Field(None, description='货币质出金额')
    FundMortgageAvailable: Optional[float] = Field(None, description='货币质押余额')
    MortgageableFund: Optional[float] = Field(None, description='可质押货币金额')
    SpecProductMargin: Optional[float] = Field(None, description='特殊产品占用保证金')
    SpecProductFrozenMargin: Optional[float] = Field(None, description='特殊产品冻结保证金')
    SpecProductCommission: Optional[float] = Field(None, description='特殊产品手续费')
    SpecProductFrozenCommission: Optional[float] = Field(None, description='特殊产品冻结手续费')
    SpecProductPositionProfit: Optional[float] = Field(None, description='特殊产品持仓盈亏')
    SpecProductCloseProfit: Optional[float] = Field(None, description='特殊产品平仓盈亏')
    SpecProductPositionProfitByAlg: Optional[float] = Field(
        None, description='根据持仓盈亏算法计算的特殊产品持仓盈亏'
    )
    SpecProductExchangeMargin: Optional[float] = Field(None, description='特殊产品交易所保证金')
    BizType: Optional[constr(max_length=1)] = Field(None, description='业务类型')
    FrozenSwap: Optional[float] = Field(None, description='延时换汇冻结金额')
    RemainSwap: Optional[float] = Field(None, description='剩余换汇额度')


class InvestorPositionField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcInvestorPositionField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    InvestorID: Optional[constr(max_length=13)] = Field(None, description='投资者代码')
    PosiDirection: Optional[constr(max_length=1)] = Field(None, description='持仓多空方向')
    HedgeFlag: Optional[constr(max_length=1)] = Field(None, description='投机套保标志')
    PositionDate: Optional[constr(max_length=1)] = Field(None, description='持仓日期')
    YdPosition: Optional[int] = Field(None, description='上日持仓')
    Position: Optional[int] = Field(None, description='今日持仓')
    LongFrozen: Optional[int] = Field(None, description='多头冻结')
    ShortFrozen: Optional[int] = Field(None, description='空头冻结')
    LongFrozenAmount: Optional[float] = Field(None, description='开仓冻结金额')
    ShortFrozenAmount: Optional[float] = Field(None, description='开仓冻结金额')
    OpenVolume: Optional[int] = Field(None, description='开仓量')
    CloseVolume: Optional[int] = Field(None, description='平仓量')
    OpenAmount: Optional[float] = Field(None, description='开仓金额')
    CloseAmount: Optional[float] = Field(None, description='平仓金额')
    PositionCost: Optional[float] = Field(None, description='持仓成本')
    PreMargin: Optional[float] = Field(None, description='上次占用的保证金')
    UseMargin: Optional[float] = Field(None, description='占用的保证金')
    FrozenMargin: Optional[float] = Field(None, description='冻结的保证金')
    FrozenCash: Optional[float] = Field(None, description='冻结的资金')
    FrozenCommission: Optional[float] = Field(None, description='冻结的手续费')
    CashIn: Optional[float] = Field(None, description='资金差额')
    Commission: Optional[float] = Field(None, description='手续费')
    CloseProfit: Optional[float] = Field(None, description='平仓盈亏')
    PositionProfit: Optional[float] = Field(None, description='持仓盈亏')
    PreSettlementPrice: Optional[float] = Field(None, description='上次结算价')
    SettlementPrice: Optional[float] = Field(None, description='本次结算价')
    TradingDay: Optional[constr(max_length=9)] = Field(None, description='交易日')
    SettlementID: Optional[int] = Field(None, description='结算编号')
    OpenCost: Optional[float] = Field(None, description='开仓成本')
    ExchangeMargin: Optional[float] = Field(None, description='交易所保证金')
    CombPosition: Optional[int] = Field(None, description='组合成交形成的持仓')
    CombLongFrozen: Optional[int] = Field(None, description='组合多头冻结')
    CombShortFrozen: Optional[int] = Field(None, description='组合空头冻结')
    CloseProfitByDate: Optional[float] = Field(None, description='逐日盯市平仓盈亏')
    CloseProfitByTrade: Optional[float] = Field(None, description='逐笔对冲平仓盈亏')
    TodayPosition: Optional[int] = Field(None, description='今日持仓')
    MarginRateByMoney: Optional[float] = Field(None, description='保证金率')
    MarginRateByVolume: Optional[float] = Field(None, description='保证金率(按手数)')
    StrikeFrozen: Optional[int] = Field(None, description='执行冻结')
    StrikeFrozenAmount: Optional[float] = Field(None, description='执行冻结金额')
    AbandonFrozen: Optional[int] = Field(None, description='放弃执行冻结')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    YdStrikeFrozen: Optional[int] = Field(None, description='执行冻结的昨仓')
    InvestUnitID: Optional[constr(max_length=17)] = Field(None, description='投资单元代码')
    PositionCostOffset: Optional[float] = Field(None, description='大商所持仓成本差值，只有大商所使用')
    TasPosition: Optional[int] = Field(None, description='tas持仓手数')
    TasPositionCost: Optional[float] = Field(None, description='tas持仓成本')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
