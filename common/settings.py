import logging

LOG_LEVEL = logging.INFO
LOG_DATE = "%Y-%m-%dT%H:%M:%S"
LOG_FORMAT = "%(asctime)s %(levelname)-8s: (%(threadName)s) [%(name)s:%(funcName)s:%(lineno)d] \t %(message)s"
LOG_FILES = {"core-debug.log": logging.DEBUG, "core-info.log": logging.INFO}
LOG_PATH = "/tmp/core/logs"
ACTION = 9
ACTION_FORMAT = "%(asctime)s.%(msecs)03d %(levelname)s    %(message)s"
