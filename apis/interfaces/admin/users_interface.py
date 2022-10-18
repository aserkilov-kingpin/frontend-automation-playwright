from typing import TYPE_CHECKING, List, Optional, Union

import requests
from common.log_handler import LogHandler

log = LogHandler.get_module_logger(__name__)

# Prevent circular import from type hints
if TYPE_CHECKING:
    from apis.interfaces.admin_client import AdminClient


class UsersInterface(object):
    def __init__(self, client: "AdminClient"):
        self.client = client

    def get_admins(self) -> dict:
        """Get all admin users

        :return: dict with user details
        """
        uri = "/adminusers" + self.client.unpack_parameters()
        response = self.client.get(uri)
        if self.client.raise_errors:
            response.raise_for_status()
        return response.json()

    def get_users(self, **kwargs) -> dict:
        """Get all users

        :return: dict with user details
        """
        uri = "/users/list" + self.client.unpack_parameters(kwargs)
        response = self.client.get(uri)
        if self.client.raise_errors:
            response.raise_for_status()
        return response.json()

    def get_user(self, user_id: str) -> dict:
        """Get user details

        :return: dict with user details
        """
        uri = f"/users/{user_id}"
        response = self.client.get(uri)
        if self.client.raise_errors:
            response.raise_for_status()
        return response.json()

    def edit_user(self, user_id: str, body) -> dict:
        """Update user

        :return: dict with response
        """
        uri = f"/users/{user_id}"
        response = self.client.patch(uri, body)
        if self.client.raise_errors:
            response.raise_for_status()
        return response.json()
