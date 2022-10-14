from common.log_handler import LogHandler
from utils.utils import restore_context, login

log = LogHandler.get_module_logger(__name__)


# def test_home_page_title(kingpin_db):
#     # Simple test, load homepage and check title
#     collection = kingpin_db.get_collection("ordersV2")
#     items = collection.find({"brandId": "6284d6a94cec9656e02ee64b"})
#     log.info([item["orderSeqId"] for item in items])
