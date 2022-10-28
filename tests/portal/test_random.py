import pytest
import csv

from common.log_handler import LogHandler
from tests.consts import MAIN_COLLECTION_PATH
from utils.utils import restore_context, login

log = LogHandler.get_module_logger(__name__)


def random():
    log.info("test")

random()
