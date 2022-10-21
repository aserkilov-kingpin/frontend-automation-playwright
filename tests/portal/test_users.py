import pytest
from playwright.sync_api import expect

from common.log_handler import LogHandler
from common.secret import SecretManager
from tests.consts import EMAIL_DOMAIN, PASSWORD_RETAILER, PASSWORD_BRAND
from utils.utils import get_current_datetime

log = LogHandler.get_module_logger(__name__)


@pytest.fixture()
def create_user(page, kingpin_db, request):
    username = request.param["username"]
    password = request.param["password"]
    phone = "12345678"
    email = f"{username}@{EMAIL_DOMAIN}"
    # page.on(
    #     "response",
    #     lambda response: print(
    #         "Response: "
    #         + response.request.url
    #         + ", Time: "
    #         + str(response.request.timing["responseStart"])
    #     ),
    # )
    page.goto("/")
    page.locator("[href='/register/']").click()
    page.locator("button", has_text=request.param["role"]).click()
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
    with page.expect_response("**/users/register**") as response_info:
        page.locator("[type='submit']").click()
    collection = kingpin_db.get_collection("users")
    yield collection.find_one({"email": email})
    collection.delete_one({"email": email})


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
    def test_retailer_registers(self, page, kingpin_db, create_user):
        if create_user is not None:
            assert create_user.get("role") == "retailer"
        else:
            pytest.fail("None user object")

    @pytest.mark.parametrize(
        "create_user",
        [{"username": brand_username, "password": brand_password, "role": "Brand"}],
        indirect=True,
    )
    def test_brand_registers(self, page, kingpin_db, create_user):
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
    def test_retailer_login(self, page, kingpin_db, create_user, admin_api_client):
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
    def test_brand_login(self, page, kingpin_db, create_user, admin_api_client):
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
