from openctp_client.objects import *
from openctp_client.objects.enums import CtpMethod
from openctp_client.apis.md_api import MdAPI

if __name__ == "__main__":
    config = CtpConfig("", "tcp://180.168.146.187:10211", "9999", "9999", "9999", "9999", "9999")
    md_api = MdAPI(config)
    
    def connected(login_info: RspUserLoginField, rsp_info: RspInfoField, request_id: int, last: bool):
        print(f"connected: {login_info.TradingDay}")
        md_api.SubscribeMarketData(["ag2308"])
    
    def on_subscribe_market_data(instrument: SpecificInstrumentField, rsp_info: RspInfoField, request_id: int, last: bool):
        print(f"subscribe market data: {instrument.model_dump_json()}")
    
    def on_market_data(data: DepthMarketDataField):
        print(f"market data: {data.model_dump_json()}")
    
    md_api.set_spi_callback(CtpMethod.OnRspUserLogin, connected)
    md_api.set_spi_callback(CtpMethod.OnRspSubMarketData, on_subscribe_market_data)
    md_api.set_spi_callback(CtpMethod.OnRtnDepthMarketData, on_market_data)
    
    md_api.Connect()
    
    ch = input("press any key to exit")
