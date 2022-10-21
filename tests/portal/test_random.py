import pytest

from common.log_handler import LogHandler
from utils.utils import restore_context, login

log = LogHandler.get_module_logger(__name__)


# @pytest.mark.custom
# def test_random(portal_api_client):
#     orders = portal_api_client.orders.get(page=0, limit=10)
#     log.info(orders)
