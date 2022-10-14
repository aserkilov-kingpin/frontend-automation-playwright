from datetime import datetime


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
