import datetime
import time
from typing import List, Optional

import requests

from apis.rest.rest_base import RestBase
from apis.rest.session_auth_base import SessionAuthBase
from common.log_handler import LogHandler
from apis.interfaces.admin.admin_base_interface import AdminBaseInterface

log = LogHandler.get_module_logger(__name__)


class AdminClient(SessionAuthBase, AdminBaseInterface):
    _SESSION_URI = "/admin/adminusers/login"

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
    ) -> None:
        super().__init__(host, username, password)
        self.raise_errors = True
        self._BASE_URI = "/admin"
        self.expected_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-XSS-Protection": "0",
            "Strict-Transport-Security": "max-age=15552000; includeSubDomains",
            "X-Frame-Options": "SAMEORIGIN",
        }

    def __str__(self) -> str:
        return f"{self.__class__.__name__} [{self.host}]"

    def unpack_parameters(self, parameters: dict = {}) -> str:
        """convert a dict into uri query params

        parameters = {"limit" = 5, "order_by" = "NAME"}

        would return "?limit=5&order_by=NAME"

        :param parameters:
        :return:
        """
        uri = ""
        first = True
        for key in parameters:
            if first:
                uri += "?"
                first = False
            else:
                uri += "&"
            if type(parameters.get(key)) is list:
                uri += f"{key}=" + f"&{key}=".join(parameters.get(key))
            else:
                uri += f"{key}={parameters.get(key)}"
        return uri
