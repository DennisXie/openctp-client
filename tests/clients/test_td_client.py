import pytest
from pytest_mock import MockerFixture
from openctp_ctp import tdapi

from openctp_client.clients.td_client import TdClient
from openctp_client.objects import *


@pytest.fixture
def td_client(config: CtpConfig, mocker: MockerFixture):
    tdapi = mocker.patch("openctp_client.clients.td_client.tdapi")
    api = mocker.Mock(name="api")
    tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi.return_value = api
