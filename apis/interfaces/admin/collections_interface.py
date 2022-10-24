from typing import TYPE_CHECKING, List, Optional, Union

import requests
from common.log_handler import LogHandler

log = LogHandler.get_module_logger(__name__)

# Prevent circular import from type hints
if TYPE_CHECKING:
    from apis.interfaces.admin_client import AdminClient


class CollectionsInterface(object):
    def __init__(self, client: "AdminClient"):
        self.client = client

    def delete(self, collection_id: str, **kwargs):
        uri = f"/catalog/collection/{collection_id}" + self.client.unpack_parameters(kwargs)
        response = self.client.delete(uri)
        if self.client.raise_errors:
            response.raise_for_status()
        return response.json()

