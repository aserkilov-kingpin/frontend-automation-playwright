import csv
import os

import pytest
from playwright.sync_api import expect

from common.log_handler import LogHandler
from common.secret import SecretManager
from tests.consts import (
    EMAIL_DOMAIN,
    PASSWORD_RETAILER,
    PASSWORD_BRAND,
    MAIN_COLLECTION_PATH,
    MAIN_COLLECTION_IMAGE_PATH,
)
from tests.portal.consts import API_URL
from utils.utils import (
    get_current_datetime,
    get_calendar_next_day,
    locator_gen,
    convert_to_currency,
)

log = LogHandler.get_module_logger(__name__)


def get_collection_product_list():
    product_list = []
    with open(MAIN_COLLECTION_PATH, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            product_list.append(
                {
                    "styleCode": row["styleCode"],
                    "descriptionShort": row["descriptionShort"],
                    "wholesalePrice": row["wholesalePrice"],
                    "retailPrice": row["retailPrice"],
                    "orderIndex": row["orderIndex"],
                }
            )
            line_count += 1
        print(f"Processed {line_count} lines.")
        return list({item["orderIndex"]: item for item in product_list}.values())


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
    page.locator(f".open [aria-label='{day}']").click()
    page.locator("#intro_collection_products").set_input_files(MAIN_COLLECTION_PATH)
    page.locator(".logo-preview").set_input_files(MAIN_COLLECTION_IMAGE_PATH)
    page.locator("button", has_text="Crop").click()
    with page.expect_response(
        lambda response: response.url == f"{API_URL}/v2/catalog/collections"
        and response.request.method == "GET"
    ) as response_info:
        page.locator("[type='submit']").click()
        response = response_info.value.json()
        collections = response.get("data").get("collections")
        collection_id = next(
            item.get("_id") for item in collections if item.get("description") == name
        )
        log.info(collection_id)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(5000)
    page.reload()
    yield page, name
    log.info(f"Deleting collection: {name}")
    admin_api_client.collections.delete(collection_id, shouldProceed="true")


def test_upload_collection(upload_collection):
    page, name = upload_collection
    expected_number = 20
    collection_locator = page.locator(".collections", has_text=name)
    products_locator = collection_locator.locator(".blog-content-truncate")
    expect(products_locator).to_have_text(f"{expected_number} Products")
    with page.expect_response(f"{API_URL}/catalog/products**") as response_info:
        collection_locator.click()
    card_locator = page.locator(".ecommerce-card")
    expect(card_locator).to_have_count(expected_number)
    i = 0
    for locator in locator_gen(card_locator):
        expected_product_list = get_collection_product_list()
        log.info(expected_product_list[i].values())
        expected_name = expected_product_list[i].get("descriptionShort")
        expected_code = expected_product_list[i].get("styleCode")
        expected_code = f"Style Code: {expected_code}"
        expected_wsp = expected_product_list[i].get("wholesalePrice")
        expected_wsp = convert_to_currency(expected_wsp)
        expected_rrp = expected_product_list[i].get("retailPrice")
        expected_rrp = str(round(float(expected_rrp)))
        expected_rrp = f"RRP: {convert_to_currency(expected_rrp)}"
        expect(locator).to_be_visible()
        image_locator = locator.locator("img")
        expect(image_locator).to_be_visible()
        name_locator = locator.locator(".product-name a")
        expect(name_locator).to_have_text(expected_name)
        code_locator = locator.locator(".product-style-code")
        expect(code_locator).to_have_text(expected_code)
        wsp_locator = locator.locator(".product-price span")
        expect(wsp_locator).to_have_text(expected_wsp)
        rrp_locator = locator.locator(".product-price-rrp")
        expect(rrp_locator).to_have_text(expected_rrp)
        i += 1
    products_found_locator = page.locator(".d-lg-block span")
    expect(products_found_locator).to_have_text(f"{expected_number} products found")
    page.wait_for_load_state("networkidle")


def test_retailer_opens_collection(browser_context):
    brand_name = "Demo Brand Arsen"
    collection_name = "Demo Brand Arsen Collection"
    context = browser_context.retailer_context
    page = context.new_page()
    page.goto("/")
    page.locator(".main-menu").hover()
    page.locator("[href='#'] .menu-title").click()
    page.locator("[href='/explore'] .menu-title").click()
    page.locator(".card-title", has_text=brand_name).scroll_into_view_if_needed()
    page.locator(".ecommerce-card", has=page.locator(".card-title", has_text=brand_name)).locator(".image").hover()
    page.locator(".card-title", has_text=brand_name).click()
    collection_locator = page.locator(".card-title", has_text=collection_name)
    expected_number = 20
    products_locator = collection_locator.locator(".blog-content-truncate")
    # expect(products_locator).to_have_text(f"{expected_number} Products")
    with page.expect_response(f"{API_URL}/catalog/products?sortBy*") as response_info:
        collection_locator.scroll_into_view_if_needed()
        collection_locator.click()
        response = response_info.value.json()
        expected_product_list = [product for products in response.get("data").get("products") for product in products.get("products")]
    card_locator = page.locator(".ecommerce-card")
    expect(card_locator).to_have_count(expected_number)
    i = 0
    for locator in locator_gen(card_locator):
        log.info(expected_product_list[i].values())
        expected_name = expected_product_list[i].get("descriptionShort")
        expected_code = expected_product_list[i].get("styleCode")
        expected_code = f"Style Code: {expected_code}"
        expected_wsp = expected_product_list[i].get("wholesalePrice")
        expected_wsp = convert_to_currency(expected_wsp)
        expected_rrp = expected_product_list[i].get("retailPrice")
        expected_rrp = str(round(float(expected_rrp)))
        expected_rrp = f"RRP: {convert_to_currency(expected_rrp)}"
        expect(locator).to_be_visible()
        image_locator = locator.locator("img")
        expect(image_locator).to_be_visible()
        name_locator = locator.locator(".product-name a")
        expect(name_locator).to_have_text(expected_name)
        code_locator = locator.locator(".product-style-code")
        expect(code_locator).to_have_text(expected_code)
        wsp_locator = locator.locator(".product-price span")
        expect(wsp_locator).to_have_text(expected_wsp)
        rrp_locator = locator.locator(".product-price-rrp")
        expect(rrp_locator).to_have_text(expected_rrp)
        i += 1
    products_found_locator = page.locator(".d-lg-block span")
    expect(products_found_locator).to_have_text(f"{expected_number} products found")
    page.wait_for_load_state("networkidle")