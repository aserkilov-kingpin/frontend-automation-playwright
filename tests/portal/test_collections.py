import os

import pytest
from playwright.sync_api import expect

from common.log_handler import LogHandler
from common.secret import SecretManager
from tests.consts import (
    EMAIL_DOMAIN,
    PASSWORD_RETAILER,
    PASSWORD_BRAND,
    MAIN_COLLECTION_PATH, MAIN_COLLECTION_IMAGE_PATH,
)
from tests.portal.consts import API_URL
from utils.utils import get_current_datetime, get_calendar_next_day

log = LogHandler.get_module_logger(__name__)


@pytest.fixture()
def upload_collection(browser_context, admin_api_client):
    name = "automation-collection-" + get_current_datetime()
    day = get_calendar_next_day()
    context = browser_context.brand_context
    page = context.new_page()
    page.goto("/")
    page.locator(".main-menu").hover()
    page.locator("[href='/collections'] .menu-title").click()
    page.locator("[href = '/collections/edit']").click()
    page.locator("#intro_collection_name").fill(name)
    page.locator("#intro_collection_description").fill(name)
    page.locator("#intro_collection_availability").click()
    page.locator("text=In Stock").click()
    page.locator("#intro_collection_end_date").click()
    page.locator(f"[aria-label='{day}']").click()
    page.locator("#intro_collection_products").set_input_files(MAIN_COLLECTION_PATH)
    page.locator(".logo-preview").set_input_files(MAIN_COLLECTION_IMAGE_PATH)
    page.locator("button", has_text="Crop").click()
    with page.expect_response(
            lambda response: response.url == f"https://{API_URL}/catalog/collections" and response.request.method == "GET") as response_info:
        page.locator("[type='submit']").click()
        response = response_info.value.json()
        collections = response.get("data")
        collection_id = next(item.get("_id") for item in collections if item.get("description") == name)
        log.info(collection_id)
    page.reload()
    yield page, page.locator(".collections", has_text=name)
    log.info(f"Deleting collection: {name}")
    admin_api_client.collections.delete(collection_id, shouldProceed="true")


@pytest.mark.custom
def test_upload_collection(upload_collection):
    page, collection_locator = upload_collection
    expected_number = 20
    products_locator = collection_locator.locator(".blog-content-truncate")
    expect(products_locator).to_contain_text(f"{expected_number} Products")
    page.wait_for_load_state("networkidle")
