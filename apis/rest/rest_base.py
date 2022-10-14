import json
import logging

import requests
from common.log_handler import LogHandler
from requests.auth import HTTPBasicAuth

log = LogHandler.get_module_logger(__name__)

logging.getLogger("urllib3").setLevel(logging.INFO)


class RestBase:
    def __init__(self, host: str, username: str = "", password: str = "") -> None:
        self.host = host
        self.username = username
        self.password = password
        self.timeout = (10, 60)
        self.secure = True
        self._BASE_URI = ""
        self.expected_headers = {}

    def __str__(self):
        return f"RestBase object at {self.host}"

    @property
    def _base_uri(self) -> str:
        """Build the base portion of a URI. Defaults to https

        set self.secure = False to use http

        :return: The base of the uri. Ex: https://1.2.3.4/api/
        """
        if self.secure:
            http = "https"
        else:
            http = "http"
        return f"{http}://{self.host}{self._BASE_URI}"

    @property
    def _is_session(self) -> bool:
        """ Method for the determining if the object uses session based auth """
        return False

    @property
    def _credentials(self) -> tuple:
        """Get a credentials tuple if username and password are set

        :return: tuple (username, password)
        """
        if self.username and self.password:
            return self.username, self.password
        return ()

    @property
    def _get_headers(self) -> dict:
        """ The header for GET operations """
        return {"Accept": "application/json"}

    @property
    def _mod_headers(self) -> dict:
        """ The header for PUT/POST/DELETE operations """
        return {"Accept": "application/json", "Content-Type": "application/json"}

    def _get_auth(self):
        """ Get either the basic auth or no auth data """
        if self._credentials:
            return HTTPBasicAuth(*self._credentials)
        return None

    def delete(self, uri: str, timeout: tuple = None) -> requests.Response:
        """Send a delete command over REST to the specified URI

        :param uri: path to send the delete to
        :param timeout: single int for both connect and read, or tuple (connect, read)
        :return: requests response object returned by delete call
        """
        if not timeout:
            timeout = self.timeout
        log.debug(f"Performing DELETE of URI: {uri} Timeout: {timeout}")
        if self._is_session:
            response = self._session.delete(self._base_uri + uri, verify=False)
        else:
            response = requests.delete(
                self._base_uri + uri,
                headers=self._mod_headers,
                verify=False,
                timeout=timeout,
            )

        log.debug(
            f"Response status: {response.status_code} Elapsed Time: {response.elapsed}"
        )

        return response

    def get(
        self, uri: str, query: dict = None, timeout: tuple = None
    ) -> requests.Response:
        """Perform a GET via REST

        :param uri: path for the request
        :param query: parameters to pass
        :param timeout: single int for both connect and read, or tuple (connect, read)
        :return: requests response object returned by delete call
        """
        if not timeout:
            timeout = self.timeout
        if self._is_session:
            log.debug(
                f"Performing session GET to URI: {uri} Timeout: {timeout} QUERY: {query}"
            )
            response = self._session.get(self._base_uri + uri, verify=False)
        else:
            log.debug(f"Performing GET to URI: {uri} Timeout: {timeout} QUERY: {query}")
            response = requests.get(
                self._base_uri + uri,
                params=query,
                verify=False,
                timeout=timeout,
            )

        log.debug(
            f"Response status: {response.status_code} Elapsed Time: {response.elapsed}"
        )

        return response

    def post(
        self,
        uri: str,
        data: dict = None,
        timeout: tuple = None,
        files=None,
        headers=None,
    ) -> requests.Response:
        """Send a REST post

        :param uri: path to send the post
        :param data: data to include in the body of the post
        :param timeout: single int for both connect and read, or tuple (connect, read)
        :param files: files in binary format to send
        :param headers: headers to set, defaults to self._mod_headers
        :return: requests response object
        """
        log.debug(f"Performing POST to URI: {uri} Timeout: {timeout} DATA: {data}")
        if headers is None:
            headers = self._mod_headers
        if self._is_session:
            response = self._session.post(
                self._base_uri + uri,
                json=data,
                headers=headers,
                files=files,
                verify=False,
            )
        else:
            auth = self._get_auth()
            response = requests.post(
                self._base_uri + uri,
                auth=auth,
                headers=headers,
                verify=False,
                json=data,
                timeout=timeout,
                files=files,
            )

        log.debug(
            f"Response status: {response.status_code} "
            f"Elapsed Time: {response.elapsed} "
            f"Headers: {response.request.headers}"
        )
        return response

    def put(
        self, uri: str, data: dict = None, timeout: tuple = None
    ) -> requests.Response:
        """Send a REST POST

        :param uri: destination to send the request
        :param data: data to include in the body
        :param timeout: single int for both connect and read, or tuple (connect, read)
        :return: requests response object returned by delete call
        """
        log.debug(f"Performing PUT to URI: {uri} Timeout: {timeout} Data: {data}")
        if not timeout:
            timeout = self.timeout
        if self._is_session:
            response = self._session.put(
                self._base_uri + uri, json=data, headers=self._mod_headers, verify=False
            )
        else:
            response = requests.put(
                self._base_uri + uri,
                headers=self._mod_headers,
                json=data,
                verify=False,
                timeout=timeout,
            )

        log.debug(
            f"Response status: {response.status_code} Elapsed Time: {response.elapsed}"
        )

        return response

    def success(self, response: requests.Response, allowed: list = None) -> bool:
        """Check to see if a response status code is in the allowed list

        :param response: requests response object to check
        :param allowed: list of allowed status code
        :return: true if response was successful, false if not
        """
        allowed = allowed or [200, 201, 202]
        return response.status_code in allowed
