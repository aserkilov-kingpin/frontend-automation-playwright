import logging
import os


LOG_LEVEL = logging.INFO
LOG_DATE = "%Y-%m-%dT%H:%M:%S"
LOG_FORMAT = "%(asctime)s %(levelname)-8s: (%(threadName)s) [%(name)s:%(funcName)s:%(lineno)d] \t %(message)s"
LOG_FILES = {"core-debug.log": logging.DEBUG, "core-info.log": logging.INFO}
LOG_PATH = "/tmp/core/logs"
ACTION = 9
ACTION_FORMAT = "%(asctime)s.%(msecs)03d %(levelname)s    %(message)s"
PASSWD_FILE = os.path.join(os.path.dirname(__file__), "secret.yaml")
PASSWD_KEY = "wqVZ1zdPq4_f9tr_74QaM8mJKzDIcVpgkkaRhsHkX2c="
