import os
import threading

from openctp_client.objects import *
from openctp_client.objects.enums import CtpMethod
from openctp_client.apis.td_api import TdAPI

connected_event = threading.Event()

def connected(login_info: RspUserLoginField, rsp_info: RspInfoField, request_id: int, is_last: bool):
    print("connected")
    connected_event.set()

def on_settlement_info(settlement_info: SettlementInfoField, rsp_info: RspInfoField, request_id: int, is_last: bool):
    if rsp_info and rsp_info.ErrorID != 0:
        print(f"error {rsp_info.model_dump()}")
    if settlement_info:
        print(settlement_info.Content)


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

td_api.Connect()
connected_event.wait()

qry_settlement_info = QrySettlementInfoField(
    BrokerID=config.broker_id,
    InvestorID=config.user_id,
    TradingDay="20230803",
)
td_api.ReqQrySettlementInfo(qry_settlement_info)
ch = input("press any key to exit\n")
