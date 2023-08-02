import queue
import threading
from enum import Enum, auto
from typing import Optional, Callable

from ..apis import MdAPI, TdAPI
from ..objects import CtpConfig
from ..objects.enums import CtpMethod
from ..objects.responses import *


class SimpleCtpClientEvent(Enum):
    on_login = auto()
    on_order = auto()
    on_trade = auto()
    on_instrument = auto()
    on_account = auto()
    on_position = auto()
    on_tick = auto()
    

# 1. 同步方式进行连接
# 2. 精简方法调用，如下单简化、合约查询简化
# 3. 事件驱动方式进行回调
# 登录、下单、撤单、查询订单、查询产品合约、查询账户、查询持仓
# 成交通知、行情通知
class SimpleCtpClient(object):
    
    def __init__(self, config: CtpConfig) -> None:
        self._config = config
        self._tdapi: TdAPI = TdAPI(config)
        self._tdapi.callback = self._produce_rsp
        self._mdapi: MdAPI = MdAPI(config)
        self._mdapi.callback = self._produce_rsp
        self._connected_lock = threading.Lock()
        self._connected_event = threading.Event()
        self._connected: bool = False
        self._connect_error: RspInfoField = None
        self._queue: queue.Queue = queue.Queue()
        self._event_callback: dict[SimpleCtpClientEvent, list[Callable]] = {
            SimpleCtpClientEvent.on_login: [],
            SimpleCtpClientEvent.on_order: [],
            SimpleCtpClientEvent.on_trade: [],
            SimpleCtpClientEvent.on_instrument: [],
            SimpleCtpClientEvent.on_account: [],
            SimpleCtpClientEvent.on_position: [],
            SimpleCtpClientEvent.on_tick: [],
        }
        self._callback: dict[CtpMethod, Callable] = {}
    
    @property
    def connected(self) -> bool:
        return self._td_connected and self._md_connected
    
    @property
    def tdapi(self) -> TdAPI:
        return self._tdapi
    
    @property
    def mdapi(self) -> MdAPI:
        return self._mdapi
    
    def log(self, *args, **kwargs) -> None:
        print(*args, **kwargs)
    
    def connect(self) -> None:
        self.mdapi.Connect()
        self._wait_connect()
        self.tdapi.Connect()
        self._wait_connect()
        
    def async_connect(self) -> None:
        self.mdapi.Connect()
        self.tdapi.Connect()
    
    def register(self, event: SimpleCtpClientEvent, callback: Callable) -> Callable:
        if callback not in self._callback[event]:
            self._callback[event].append(callback)
        return callback
    
    def unregister(self, event: SimpleCtpClientEvent, callback: Callable) -> None:
        if callback in self._callback[event]:
            self._callback[event].remove(callback)
    
    def _wait_connect(self) -> None:
        self._connected_event.wait()
        self._connected_event.clear()
        if not self._connected and self._connect_error:
            raise Exception(self._connect_error)
   
    def _produce_rsp(self, rsp: CtpResponse) -> None:
        self._queue.put(rsp)
    
    def _consume_rsp(self) -> None:
        while True:
            rsp = self._queue.get()
            if rsp:
                self._process_rsp(rsp)
            else:
                break
    
    def _process_rsp(self, rsp: CtpResponse) -> None:
        if rsp.method in self._callback:
            self._callback[rsp.method](rsp)
    
    def _authenticate(self, rsp: RspAuthenticate) -> None:
        pass
    
    def _login(self, rsp: RspUserLogin) -> None:
        if rsp.ok:
            with self._connected_lock:
                self._connected = True
            self.log(f"Connect to {rsp.source} success.")
        else:
            self._login_failed(rsp.rsp_info)
        self._connected_event.set()
    
    def _login_failed(self, rsp_info: RspInfoField) -> None:
        self._connect_error = rsp_info
    
    def _on_tick(self) -> None:
        pass
