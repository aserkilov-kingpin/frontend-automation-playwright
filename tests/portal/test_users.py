import pytest
from playwright.sync_api import expect, BrowserContext
from common.log_handler import LogHandler
from tests.consts import EMAIL_DOMAIN, PASSWORD_RETAILER, PASSWORD_BRAND, LOGIN_RETAILER, LOGIN_BRAND
from tests.portal.consts import API_URL
from utils.utils import get_current_datetime

log = LogHandler.get_module_logger(__name__)


@pytest.fixture()
def create_user(browser_context, kingpin_db, page, request) -> dict:
    username = request.param["username"]
    password = request.param["password"]
    role = request.param["role"]
    log.info("Running create_user")
    phone = "12345678"
    email = f"{username}@{EMAIL_DOMAIN}"
    page.goto("/")
    page.locator("[href='/register/']").click()
    page.locator("button", has_text=role).click()
    page.locator("input").fill(username)
    page.locator("[type='submit']").click()
    page.locator("[placeholder='First Name']").fill(username)
    page.locator("[placeholder='Last Name']").fill(username)
    page.locator("[placeholder='Country']").click()
    page.locator("li", has_text="Andorra").click()
    page.locator("[name='telephone']").fill(phone)
    page.locator("[type='submit']").click()
    page.locator("[type='email']").fill(email)
    page.locator("[placeholder='Password']").fill(password)
    page.locator("[placeholder='Re-enter Password']").fill(password)
    page.locator(".checkmark").check()
    with page.expect_response(f"{API_URL}/users/register") as response_info:
        page.locator("[type='submit']").click()
    collection = kingpin_db.get_collection("users")
    yield collection.find_one({"email": email})
    collection.delete_one({"email": email})


def check_existing_user(context: BrowserContext, role: str, username: str, password: str):
    response_list = []
    context.set_default_navigation_timeout(120000)
    page = context.new_page()
    page.on("response", lambda response: response_list.append(response))
    page.goto("/")
    page.locator('.cursor-pointer').click()
    page.locator('[name="login-email"]').fill(username)
    page.locator('[name="login-password"]').fill(password)
    page.locator('[type="submit"]').click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url("/dashboard")
    order_rows_locator = page.locator(".card table tbody tr")
    assert order_rows_locator.count() > 1
    # Wishlists for retailer and collections for brand
    rows_locator = page.locator(".list-group-item span")
    assert rows_locator.count() > 1
    upcoming_rows_locator = page.locator(".upcoming-deadlines table tbody tr")
    if role == "retailer":
        assert upcoming_rows_locator.count() > 1
    else:
        assert upcoming_rows_locator.count() == 0
    dashboard_url = f"{API_URL}/dashboard"
    collection_url = f"{API_URL}/catalog/collection-deadline-list"
    dashboard_response = next(
        (
            response.url
            for response in response_list
            if dashboard_url in response.url
        ),
        None,
    )
    collection_response = next(
        (
            response.json()
            for response in response_list
            if collection_url in response.url
        ),
        None,
    )


class TestUsers:
    retailer_username = "automation-retailer-" + get_current_datetime()
    retailer_password = PASSWORD_RETAILER
    brand_username = "automation-brand-" + get_current_datetime()
    brand_password = PASSWORD_BRAND

    @pytest.mark.parametrize(
        "create_user",
        [
            {
                "username": retailer_username,
                "password": retailer_password,
                "role": "Retailer",
            }
        ],
        indirect=True,
    )
    def test_retailer_registers(self, create_user):
        if create_user is not None:
            assert create_user.get("role") == "retailer"
        else:
            pytest.fail("None user object")

    @pytest.mark.parametrize(
        "create_user",
        [{"username": brand_username, "password": brand_password, "role": "Brand"}],
        indirect=True,
    )
    def test_brand_registers(self, create_user):
        if create_user is not None:
            assert create_user.get("role") == "brand"
        else:
            pytest.fail("None user object")

    @pytest.mark.parametrize(
        "create_user",
        [
            {
                "username": retailer_username,
                "password": retailer_password,
                "role": "Retailer",
            }
        ],
        indirect=True,
    )
    def test_retailer_login(self, page, create_user, admin_api_client):
        body = {"status": "approved"}
        admin_api_client.users.edit_user(str(create_user["_id"]), body=body)
        email = f"{self.retailer_username}@{EMAIL_DOMAIN}"
        page.goto("/")
        page.locator('[name="login-email"]').fill(email)
        page.locator('[name="login-password"]').fill(self.retailer_password)
        page.locator('[type="submit"]').click()
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url("/dashboard")
        welcome_locator = page.locator(".for-welcome-content")
        expect(welcome_locator).to_be_visible()

    @pytest.mark.parametrize(
        "create_user",
        [{"username": brand_username, "password": brand_password, "role": "Brand"}],
        indirect=True,
    )
    def test_brand_login(self, page, create_user, admin_api_client):
        body = {"status": "approved"}
        admin_api_client.users.edit_user(str(create_user["_id"]), body=body)
        email = f"{self.brand_username}@{EMAIL_DOMAIN}"
        page.goto("/")
        page.locator('[name="login-email"]').fill(email)
        page.locator('[name="login-password"]').fill(self.brand_password)
        page.locator('[type="submit"]').click()
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url("/dashboard")
        welcome_locator = page.locator(".for-welcome-content")
        expect(welcome_locator).to_be_visible()

    def test_existing_retailer_login(self, context):
        check_existing_user(context, "retailer", LOGIN_RETAILER, PASSWORD_RETAILER)


    def test_existing_brand_login(self, context):
        check_existing_user(context, "brand", LOGIN_BRAND, PASSWORD_BRAND)
