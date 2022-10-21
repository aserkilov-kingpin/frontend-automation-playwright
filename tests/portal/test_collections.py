import pytest
from playwright.sync_api import expect

from common.log_handler import LogHandler
from common.secret import SecretManager
from tests.consts import EMAIL_DOMAIN, PASSWORD_RETAILER, PASSWORD_BRAND
from utils.utils import get_current_datetime

log = LogHandler.get_module_logger(__name__)


@pytest.mark.custom
def test_upload_collection(browser_context):
    context = browser_context.brand_context
    page = context.new_page()
    page.goto("/")
    # page.locator(".feather-menu").click()
    page.locator(".main-menu").hover()
    page.locator("[href='/collections'] .menu-title").click()
    page.locator("[href = '/collections/edit']").click()
    page.wait_for_load_state("networkidle")
