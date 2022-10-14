from typing import TYPE_CHECKING, List, Optional, Union

import requests
from common.log_handler import LogHandler

log = LogHandler.get_module_logger(__name__)

# Prevent circular import from type hints
if TYPE_CHECKING:
    from apis.interfaces.portal_client import PortalClient


class OrdersInterface(object):
    def __init__(self, client: "PortalClient"):
        self.client = client

    def get(self, **kwargs) -> dict:
        """Get all user orders

        :return: dict with orders details
        """
        uri = "/v2/orders" + self.client.unpack_parameters(kwargs)
        response = self.client.get(uri)
        if self.client.raise_errors:
            response.raise_for_status()
        return response.json()
