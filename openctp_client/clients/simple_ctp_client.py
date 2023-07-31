import threading
from typing import Optional

from ..apis import MdAPI, TdAPI
from ..objects import CtpConfig


class SimpleCtpClient(object):
    
    def __init__(self, config: CtpConfig) -> None:
        self._config = config
        self._tdapi: TdAPI = TdAPI(config)
        self._mdapi: MdAPI = MdAPI(config)
        self._connected_lock = threading.Lock()
        self._connected_event = threading.Event()
        self._td_connected: bool = False
        self._md_connected: bool = False
    
    @property
    def connected(self) -> bool:
        return self._td_connected and self._md_connected
    
    @property
    def tdapi(self) -> Optional[TdAPI]:
        return self._tdapi
    
    @property
    def mdapi(self) -> Optional[MdAPI]:
        return self._mdapi
    
    def connect(self) -> None:
        self.tdapi.Connect()
        self.mdapi.Connect()
