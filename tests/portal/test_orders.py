import pytest

from common.log_handler import LogHandler

log = LogHandler.get_module_logger(__name__)


# class TestOrders:
#     def test_orders_page(self, browser_context):
#         # context = browser.new_context(storage_state="state.json")
#         # page = context.new_page()
#         # login(page)
#         # page.goto("/orders")
#         retailer_context = browser_context.retailer_context
#         page = retailer_context.new_page()
#         with page.expect_response("**/v2/orders**") as response_info:
#             page.goto(pytest.host + "/orders")
#             response = response_info.value.json()
#         rows = page.locator("table tbody tr").count()
#         count = response["data"]["count"]
#         if count < 10:
#             assert rows == count
#         else:
#             assert rows == 10
#         page.close()
#
#     def test_shipments_page(self, browser_context):
#         retailer_context = browser_context.retailer_context
#         page = retailer_context.new_page()
#         with page.expect_response("**/v2/shipments**") as response_info:
#             page.goto(pytest.host + "/shipments")
#             response = response_info.value.json()
#         rows = page.locator("table tbody tr").count()
#         count = response["data"]["count"]
#         if count < 10:
#             assert rows == count
#         else:
#             assert rows == 10
#         page.close()
