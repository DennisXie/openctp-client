import os
import threading
import openctp_client.openctp
from openctp_tts import tdapi
openctp_client.openctp.tdapi = tdapi

from openctp_client.objects import *
from openctp_client.objects.enums import CtpMethod
from openctp_client.clients import SimpleCtpClient, SimpleCtpClientEvent


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
        self.event = threading.Event()
    
    def main(self):
        self.client.connect()
        # self.client.subscribe("ag2312")
    
    def on_tick(self, tick):
        print(tick.model_dump())


if __name__ == "__main__":
    demo = OrderInsertDemo()
    demo.main()
    ch = input("press enter to exit")
    demo.client.disconnect()
