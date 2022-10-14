import logging
import logging.handlers
import os
import sys

from .settings import ACTION, LOG_DATE, LOG_FILES, LOG_FORMAT, LOG_LEVEL, LOG_PATH

logging.getLogger("paramiko").setLevel(logging.WARNING)


class LogHandler:
    @staticmethod
    def get_script_logger(log_level=LOG_LEVEL, script_log: str = "") -> logging.Logger:
        """Create a logger for a script. This will control the log level printed to the screen as well
        as create a file in the log dir called script_log

        Ex:

            import logging
            from core.common.log_handler import LogHandler
            log = LogHandler.get_script_logger(logging.DEBUG, "example.log")

            log.debug("this is a debug log")

        :param log_level: the logging level to display to the screen and store in the script log
        :param script_log: name of the file to write logs inside LOG_DIR or LOG_PATH
        :return: Logger to use for logging
        """
        log_format = "%(asctime)s %(levelname)-8s: %(message)s"
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(logging.Formatter(log_format))
        logger = logging.getLogger()
        # Level needs to be set for logger as well, it doesn't seem to take from the corresponding handlers!
        logger.setLevel(log_level)
        logger.addHandler(stream_handler)

        log_path = os.environ.get("LOG_DIR", LOG_PATH)
        os.makedirs(log_path, exist_ok=True)
        if script_log:
            file_path = os.path.join(log_path, script_log)
            file_handler = logging.handlers.RotatingFileHandler(
                file_path, mode="w", maxBytes=52428800, backupCount=10
            )
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(LOG_FORMAT, LOG_DATE)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger

    @staticmethod
    def get_module_logger(name: str) -> logging.Logger:
        """Create a logger for an internal module.

        Ex:
            from core.common.log_handler import LogHandler
            log = LogHandler.get_module_logger(__name__)

            log.debug("this is a debug log")

        :param name: the module name to use in the logger, usually __name__
        :return: Logger to use for logging
        """
        logging.captureWarnings(True)

        logger = logging.getLogger(name)
        logger.setLevel(ACTION)
        # make log dirs
        log_path = os.environ.get("LOG_DIR", LOG_PATH)
        os.makedirs(log_path, exist_ok=True)
        for log in LOG_FILES:
            file_path = os.path.join(log_path, log)
            file_handler = logging.handlers.RotatingFileHandler(
                file_path, mode="w", maxBytes=52428800, backupCount=10
            )
            file_handler.setLevel(LOG_FILES[log])
            formatter = logging.Formatter(LOG_FORMAT, LOG_DATE)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger

    @staticmethod
    def get_log_dir():
        """Get the path used for logging"""
        return os.environ.get("LOG_DIR", LOG_PATH)
