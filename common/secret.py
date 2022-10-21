import ctypes
import os
import re
import sys

import yaml
from utils.yaml import load_yaml
from cryptography.fernet import Fernet

from common.settings import PASSWD_FILE, PASSWD_KEY


class SecretManager:
    @property
    def fernet(self) -> Fernet:
        if not hasattr(self, "_fernet"):
            self._fernet = Fernet(self.key)
        return self._fernet

    @property
    def config(self) -> dict:
        if not hasattr(self, "_config"):
            self._config = load_yaml(PASSWD_FILE)
        return self._config

    @property
    def passwords(self):
        return self.config.get("Passwords")

    @property
    def key(self):
        return PASSWD_KEY.encode()

    def get_password(self, name: str) -> str:
        """Get a password from the secret manager

        :param name: name used to store the password
        :return: password in plaintext
        """
        password_enc = self.passwords.get(name)
        return self.fernet.decrypt(password_enc.encode()).decode().replace("\\n", "\n")

    def add_password(self, name: str, password: str):
        """Add or update a password in the PASSWD_FILE

        :param name: name used to refer to the password
        :param password: The new password in plantext
        :return:
        """
        password_enc = self.fernet.encrypt(password.encode()).decode()
        self.passwords[name] = password_enc
        self._write_file()

    def _write_file(self):
        """Store the changes to PASSWD_FILE"""
        with open(PASSWD_FILE, "w") as fh:
            yaml.dump(self.config, fh)


# fernet = Fernet("wqVZ1zdPq4_f9tr_74QaM8mJKzDIcVpgkkaRhsHkX2c=")
# print(
#     fernet.decrypt(
#         "gAAAAABjUo_N1S2-822n_mfXHUNqasVbOgfeQDILSj-jCyN-_JdS9LIWcNfajWwJBd_TwIZR4pK8LtTnGLjvtGX-qm9XDb68zg==".encode()
#     )
#     .decode()
#     .replace("\\n", "\n")
# )
