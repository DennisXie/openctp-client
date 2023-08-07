import queue
import threading
from enum import Enum, auto
from typing import Optional, Callable

from ..apis import MdAPI, TdAPI
from ..exceptions import CtpException
from ..objects import CtpConfig
from ..objects.enums import CtpMethod
from ..objects.responses import *


class SimpleCtpClientEvent(Enum):
    on_connected = auto()
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
            SimpleCtpClientEvent.on_connected: [],
            SimpleCtpClientEvent.on_order: [],
            SimpleCtpClientEvent.on_trade: [],
            SimpleCtpClientEvent.on_instrument: [],
            SimpleCtpClientEvent.on_account: [],
            SimpleCtpClientEvent.on_position: [],
            SimpleCtpClientEvent.on_tick: [],
        }
        self._ctp_callback: dict[CtpMethod, Callable] = {
            CtpMethod.OnRspUserLogin: self._login,
            CtpMethod.OnRspAuthenticate: self._authenticate,
            CtpMethod.OnRtnDepthMarketData: self._on_tick,
        }
        self._thread = threading.Thread(target=self._consume_rsp)
    
    @property
    def connected(self) -> bool:
        return self._connected
    
    @property
    def tdapi(self) -> TdAPI:
        return self._tdapi
    
    @property
    def mdapi(self) -> MdAPI:
        return self._mdapi
    
    def log(self, *args, **kwargs) -> None:
        print(*args, **kwargs)
    
    def on_ctp_event(self, method: CtpMethod, callback: Callable) -> Callable:
        self._ctp_callback[method] = callback
    
    def on_event(self, event: SimpleCtpClientEvent, callback: Callable) -> Callable:
        if callback not in self._event_callback[event]:
            self._event_callback[event].append(callback)
    
    def off_event(self, event: SimpleCtpClientEvent, callback: Callable) -> Callable:
        if callback in self._event_callback[event]:
            self._event_callback[event].remove(callback)
    
    def connect(self) -> None:
        self._start_process()
        self.mdapi.Connect()
        self._wait_connect()
        self.tdapi.Connect()
        self._wait_connect()
    
    def disconnect(self) -> None:
        # TODO: disconnect api
        self._stop_process()
        
    def async_connect(self) -> None:
        self.mdapi.Connect()
        self.tdapi.Connect()
    
    def subscribe(self, *instruments: list[str]) -> None:
        self.mdapi.SubscribeMarketData(instruments)
        
    def _wait_connect(self) -> None:
        self._connected_event.wait()
        self._connected_event.clear()
        if not self._connected and self._connect_error:
            raise CtpException(self._connect_error.ErrorID, self._connect_error.ErrorMsg)

    def _start_process(self) -> None:
        self._thread.start()
    
    def _stop_process(self) -> None:
        self._queue.put(None)

    def _produce_rsp(self, rsp: CtpResponse) -> None:
        self.log(f"Produce rsp: {rsp.method}")
        self._queue.put(rsp)
    
    def _consume_rsp(self) -> None:
        while True:
            rsp = self._queue.get()
            if rsp:
                self._process_rsp(rsp)
            else:
                break
    
    def _process_rsp(self, rsp: CtpResponse) -> None:
        if rsp.method in self._ctp_callback:
            self._ctp_callback[rsp.method](rsp)
        else:
            self.log(f"Method {rsp.method} not support, skipped.")
    
    def _authenticate(self, rsp: RspAuthenticate) -> None:
        self.log(f"Td authenticate failed.")
        self._login_failed(rsp.RspInfo, Api.Td)
    
    def _login(self, rsp: RspUserLogin) -> None:
        self.log(f"Login to {rsp.source.name}.")
        if rsp.ok:
            self._login_success(rsp.RspUserLogin, rsp.source)
        else:
            self._login_failed(rsp.RspInfo, rsp.source)
    
    def _login_success(self, login_field: RspUserLoginField, source: Api) -> None:
        self.log(f"Connect to {source.name} success.")
        with self._connected_lock:
            self._connected = True
        self._connected_event.set()
       
    
    def _login_failed(self, rsp_info: RspInfoField, source: Api) -> None:
        self.log(f"Connect to {source.name} failed.")
        with self._connected_lock:
            self._connected = False
            self._connect_error = rsp_info
        self._connected_event.set()
    
    def _on_tick(self, rsp: RtnDepthMarketData) -> None:
        for callback in self._event_callback[SimpleCtpClientEvent.on_tick]:
            callback(rsp.DepthMarketData)
