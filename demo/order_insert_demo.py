import os
import threading
import openctp_client.openctp
from openctp_tts import tdapi
openctp_client.openctp.tdapi = tdapi

from openctp_client.objects import *
from openctp_client.objects.enums import CtpMethod
from openctp_client.objects.responses import *
from openctp_client.clients import SimpleCtpClient, SimpleCtpClientEvent
from openctp_client.clients.simple_ctp_client import Direction, Offset


class OrderInsertDemo(object):
    
    def __init__(self) -> None:
        config = CtpConfig(
            td_addr = "tcp://42.192.226.242:20002",
            md_addr = "tcp://140.207.168.9:42213",
            broker_id="9999",
            auth_code="0000000000000000",
            app_id="simnow_client_test",
            user_id=os.getenv("CTP_USER_ID"),
            password=os.getenv("CTP_PASSWORD"),
        )
        self.client = SimpleCtpClient(config)
        self.client.on_event(SimpleCtpClientEvent.on_tick, self.on_tick)
        self.client.on_ctp_event(CtpMethod.OnRspQryDepthMarketData, self.on_qry_depth_market_data)
        self.client.on_ctp_event(CtpMethod.OnRspOrderInsert, self.on_rsp_order_insert)
        self.client.on_ctp_event(CtpMethod.OnErrRtnOrderInsert, self.on_err_rtn_order_insert)
        self.client.on_ctp_event(CtpMethod.OnRtnOrder, self.on_rtn_order)
        self.event = threading.Event()
    
    def main(self):
        self.client.connect()
        req = QryDepthMarketDataField(InstrumentID="ag2312", ExchangeID="SHFE")
        self.client.tdapi.ReqQryDepthMarketData(req)
        # self.client.subscribe("ag2312")
    
    def on_tick(self, tick):
        print(tick.model_dump())
    
    def on_qry_depth_market_data(self, rsp: RspQryDepthMarketData):
        market_data = rsp.DepthMarketData
        price = int(market_data.BidPrice1 * 1.01) * 1.0
        print(f"insert a order for price {price}")
        self.client.order_insert("SHFE", "ag2312", price, 1, Direction.Sell, Offset.CloseToday)
    
    def on_rsp_order_insert(self, rsp: RspOrderInsert):
        print(rsp.model_dump())
    
    def on_err_rtn_order_insert(self, rsp: RspOrderInsert):
        print(rsp.model_dump())
    
    def on_rtn_order(self, rsp: RtnOrder):
        o = rsp.Order
        print("==============================on_rtn_order==============================")
        print(f"FrontID: {o.FrontID} SessionID: {o.SessionID} OrderRef: {o.OrderRef}")
        print(f"ExchangeID: {o.ExchangeID} TraderID: {o.TraderID} OrderLocalID: {o.OrderLocalID}")
        print(f"OrderSysID: {o.OrderSysID}")
        print(f"OrderSubmitStatus: {o.OrderSubmitStatus} Direction: {o.Direction} Offset: {o.CombOffsetFlag}")

if __name__ == "__main__":
    demo = OrderInsertDemo()
    demo.main()
    ch = input("press enter to exit")
    demo.client.disconnect()
