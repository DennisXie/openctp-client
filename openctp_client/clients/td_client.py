from typing import Callable, Tuple
from openctp_ctp import tdapi

from ..objects.config import CtpConfig
from ..objects.enums import CtpMethod
from ..objects.fields import *
from ..objects.responses import *


class TdClient(tdapi.CThostFtdcTraderSpi):
    
    def __init__(self) -> None:
        super().__init__()
