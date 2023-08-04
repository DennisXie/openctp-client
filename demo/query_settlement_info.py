import os
import threading

from openctp_client.objects import *
from openctp_client.objects.enums import CtpMethod
from openctp_client.apis.td_api import TdAPI

connected_event = threading.Event()
settlement_event = threading.Event()

def connected(login_info: RspUserLoginField, rsp_info: RspInfoField, request_id: int, is_last: bool):
    print("connected")
    connected_event.set()

def on_settlement_info(settlement_info: SettlementInfoField, rsp_info: RspInfoField, request_id: int, is_last: bool):
    if rsp_info and rsp_info.ErrorID != 0:
        print(f"error {rsp_info.model_dump()}")
    if settlement_info:
        # pydantic这里的content是deepcopy的，不会存在ctp复用内存导致已经保存的数据被覆盖的问题
        print(settlement_info.Content)
    if is_last:
        settlement_event.set()

def on_settlement_confirm(settlement_info_confirm: SettlementInfoConfirmField, rsp_info: RspInfoField, request_id: int, is_last: bool):
    if rsp_info:
        print(f"settlement confirm error {rsp_info.model_dump()}")
    if settlement_info_confirm:
        print(settlement_info_confirm.model_dump())    


config = CtpConfig(
    td_addr="tcp://180.168.146.187:10201",
    md_addr="",
    broker_id="9999",
    auth_code="0000000000000000",
    app_id="simnow_client_test",
    user_id=os.getenv("CTP_USER_ID"),
    password=os.getenv("CTP_PASSWORD"),
)

td_api = TdAPI(config=config)
td_api.set_spi_callback(CtpMethod.OnRspUserLogin, connected)
td_api.set_spi_callback(CtpMethod.OnRspQrySettlementInfo, on_settlement_info)
td_api.set_spi_callback(CtpMethod.OnRspQrySettlementInfoConfirm, on_settlement_confirm)

td_api.Connect()
connected_event.wait()

qry_settlement_info = QrySettlementInfoField(
    BrokerID=config.broker_id,
    InvestorID=config.user_id,
    TradingDay="20230803",
)
td_api.ReqQrySettlementInfo(qry_settlement_info)
settlement_event.wait()
ch = input("press to confirm settlement info\n")
settlement_info_confirm = QrySettlementInfoConfirmField(
    BrokerID=config.broker_id,
    InvestorID=config.user_id,
    AccountID=config.user_id,
)
td_api.ReqQrySettlementInfoConfirm(settlement_info_confirm)
ch = input("press any key to exit\n")
