import pytest

from common.log_handler import LogHandler
from utils.utils import get_current_datetime

log = LogHandler.get_module_logger(__name__)


@pytest.fixture()
def create_user(page, kingpin_db, request):
    username = request.param["username"]
    password = request.param["password"]
    phone = "12345678"
    email_domain = "@kingpin.global"
    email = username + email_domain
    page.goto("/")
    page.locator("[href='/register/']").click()
    page.locator("button", has_text="Retailer").click()
    page.locator("input").fill(username)
    page.locator("[type='submit']").click()
    page.locator("[placeholder='First Name']").fill(username)
    page.locator("[placeholder='Last Name']").fill(username)
    page.locator("[placeholder='Country']").click()
    page.locator("li", has_text="Andorra").click()
    page.locator("[name='telephone']").fill(phone)
    page.locator("[type='submit']").click()
    page.locator("[type='email']").fill(username + email_domain)
    page.locator("[placeholder='Password']").fill(password)
    page.locator("[placeholder='Re-enter Password']").fill(password)
    page.locator(".checkmark").check()
    with page.expect_response("**/users/register**") as response_info:
        page.locator("[type='submit']").click()
    collection = kingpin_db.get_collection("users")
    yield collection.find_one({"email": email})
    collection.delete_one({"email": email})


class TestUsers:
    username = "automation-retailer-" + get_current_datetime()
    password = pytest.retailer_password

    @pytest.mark.parametrize("create_user", [{"username": username, "password": password}], indirect=True)
    def test_retailer_registers(self, page, kingpin_db, create_user):
        assert create_user

    username = "automation-brand-" + get_current_datetime()
    password = pytest.brand_password

    @pytest.mark.parametrize("create_user", [{"username": username, "password": password}], indirect=True)
    def test_brand_registers(self, page, kingpin_db, create_user):
        assert create_user
