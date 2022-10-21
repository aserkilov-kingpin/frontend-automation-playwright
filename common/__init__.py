import sys
import traceback

from common.log_handler import LogHandler


def my_exception_hook(type, value, tb):
    logger = LogHandler.get_module_logger(__name__)
    logger.exception(f"{''.join(traceback.format_exception(type, value, tb))}")
    # print(f"{type}  {value}  {tb}")
    print(f"{''.join(traceback.format_exception(type, value, tb))}")


sys.excepthook = my_exception_hook
