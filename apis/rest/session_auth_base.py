from apis.rest.rest_base import RestBase
from common.log_handler import LogHandler
from requests import Session

log = LogHandler.get_module_logger(__name__)


class SessionAuthBase(RestBase):
    def __init__(self, host: str, username: str, password: str) -> None:
        super().__init__(host, username, password)

    @property
    def _session_uri(self) -> str:
        """Gets the session_uri"""
        session_uri = getattr(self, "_SESSION_URI", "")
        return f"https://{self.host}{session_uri}"

    @property
    def _is_session(self) -> bool:
        """Method for the determining if the object uses session based auth"""
        return True

    @property
    def _session(self) -> Session:
        """Get an existing session, or create a new one
        Force a new session with delattr(self, '_session_')

        :return: requests session
        """
        if not hasattr(self, "_session_"):
            self._session_ = Session()
            self._session_.verify = False
            self._session_.headers.update(self._get_headers)
            response = self._session_.post(
                self._session_uri,
                data={"email": self.username, "password": self.password},
                timeout=30,
            )
            access_token = "Bearer " + response.json()["data"]["token"]
            self._session_.headers.update({"Authorization": access_token})
            if not self.success(response):
                # TODO: Make uniform exceptions
                log.error(f"create session failed: {response.reason}")
                raise ConnectionError(
                    f"create session failed: {response.reason}, check user/pass is set correct"
                )

            log.debug(
                f"Created session for {self}:{self._credentials}:{response.headers}"
            )
        # TODO: Make sure the session is valid/alive?
        return self._session_

    def clear_session(self):
        """Delete the existing session details to force a new authentication"""
        if hasattr(self, "_session_"):
            delattr(self, "_session_")
