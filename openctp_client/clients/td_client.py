from typing import Callable, Tuple
from openctp_ctp import tdapi

from ..objects.config import CtpConfig
from ..objects.enums import CtpMethod
from ..objects.fields import *
from ..objects.responses import *


class TdClient(tdapi.CThostFtdcTraderSpi):
    
    def __init__(self, config: CtpConfig) -> None:
        super().__init__()
        self.config = config
        self._request_count = 0
        self._callback = self._default_callback
        self._spi_callback: dict[CtpMethod, Callable] = {}
    
    @property
    def request_id(self) -> int:
        self._request_count += 1
        return self._request_count
    
    @property
    def callback(self) -> Callable:
        return self._callback
    
    @callback.setter
    def callback(self, callback: Callable) -> None:
        self._callback = callback
    
    def _default_callback(self) -> None:
        pass
    
    def set_spi_callback(self, method: CtpMethod, callback: Callable):
        self._spi_callback[method] = callback
    
    def get_spi_callback(self, method: CtpMethod) -> Callable | None:
        return self._spi_callback.get(method)
    
    def del_spi_callback(self, method: CtpMethod) -> Callable | None:
        return self._spi_callback.pop(method, None)
