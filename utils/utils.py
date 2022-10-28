from datetime import datetime, timedelta

from playwright.sync_api import Locator


def login(page):
    page.locator('[name="login-email"]').fill(pytest.username)
    page.locator('[name="login-password"]').fill(pytest.password)
    login_locator = page.locator('[type="submit"]')
    login_locator.click(force=True)
    page.wait_for_load_state("networkidle")


def restore_context(browser):
    return browser.new_context(storage_state="state.json")


def get_current_datetime():
    now = datetime.now()
    return now.strftime("%H%M%S%d%m%Y")


def get_calendar_next_day():
    today = datetime.today() + timedelta(days=1)
    return today.strftime(f"%B {today.day}, %Y")


def locator_gen(locator: Locator):
    for i in range(0, locator.count()):
        yield locator.nth(i)


def convert_to_currency(number: str):
    return "${:.2f}".format(float(number))
