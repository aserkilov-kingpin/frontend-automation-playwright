import json
from collections import namedtuple

import playwright
import requests
from pytest_playwright.pytest_playwright import _build_artifact_test_folder

from apis.interfaces.admin_client import AdminClient
from apis.interfaces.portal_client import PortalClient
from common.log_handler import LogHandler
from os import getenv
from requests import exceptions, post
import pytest
import re
from playwright.sync_api import Playwright, sync_playwright
from playwright.sync_api import BrowserType
from typing import Dict, Any, Optional
import shutil
import os
import sys
import warnings
from typing import Any, Callable, Dict, Generator, List, Optional

import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    BrowserType,
    Error,
    Page,
    Playwright,
    sync_playwright,
)
from slugify import slugify
import tempfile

from pymongo import MongoClient

from tests.consts import MONGODB_CONNECTION_STRING

log = LogHandler.get_module_logger(__name__)
artifacts_folder = tempfile.TemporaryDirectory(prefix="playwright-pytest-")


def pytest_addoption(parser):
    group_admin = parser.getgroup("Frontend Testing")
    group_admin.addoption("--host", action="store", help="Frontend host address")
    group_admin.addoption("--api", action="store", help="Backend host address")
    group_admin.addoption(
        "--retailer-username",
        action="store",
        help="Retailer Username",
    )
    group_admin.addoption(
        "--retailer-password",
        action="store",
        help="Retailer Password",
    )
    group_admin.addoption(
        "--brand-username",
        action="store",
        help="Brand Username",
    )
    group_admin.addoption(
        "--brand-password",
        action="store",
        help="Brand Password",
    )


def pytest_configure(config):
    if config.getoption("--base-url"):
        base_url = config.getoption("base_url")
    else:
        base_url = getenv("base_url")
    if config.getoption("--host"):
        host = config.getoption("host")
    else:
        host = getenv("host")
    if config.getoption("--api"):
        api = config.getoption("api")
    else:
        api = getenv("api")
    if config.getoption("--retailer-username"):
        retailer_username = config.getoption("retailer_username")
    else:
        retailer_username = getenv("retailer_username")
    if config.getoption("--retailer-password"):
        retailer_password = config.getoption("retailer_password")
    else:
        retailer_password = getenv("retailer_password")
    if config.getoption("--brand-username"):
        brand_username = config.getoption("brand_username")
    else:
        brand_username = getenv("brand_username")
    if config.getoption("--brand-password"):
        brand_password = config.getoption("brand_password")
    else:
        brand_password = getenv("brand_password")
    if base_url is None:
        print("No host (--base-url option or 'base_url' env variable)")
    if host is None:
        print("No host (--host option or 'host' env variable)")
    if api is None:
        print("No api (--api option or 'api' env variable)")
    if retailer_username is None:
        print(
            "No retailer_username (--retailer-username option or 'retailer_username' env variable)"
        )
    if retailer_password is None:
        print(
            "No retailer_password (--retailer-password option or 'retailer_password' env variable)"
        )
    if brand_username is None:
        print(
            "No brand_username (--brand-username option or 'brand_username' env variable)"
        )
    if brand_password is None:
        print(
            "No brand_password (--brand-password option or 'brand_password' env variable)"
        )
    pytest.base_url = base_url
    pytest.host = host
    pytest.api = api
    pytest.retailer_username = retailer_username
    pytest.retailer_password = retailer_password
    pytest.brand_username = brand_username
    pytest.brand_password = brand_password


@pytest.fixture(scope="session")
def admin_api_client(pytestconfig) -> AdminClient:
    host = pytest.host
    username = pytestconfig.getoption("username")
    password = pytestconfig.getoption("password")
    try:
        app = AdminClient(host=host, username=username, password=password)
    except exceptions.ConnectionError as e:
        raise ConnectionError(f"Failed to connect to {host}")
    yield app


@pytest.fixture(scope="session")
def portal_api_client(pytestconfig) -> PortalClient:
    host = pytest.host
    username = pytestconfig.getoption("username")
    password = pytestconfig.getoption("password")
    try:
        app = PortalClient(host=host, username=username, password=password)
    except exceptions.ConnectionError as e:
        raise ConnectionError(f"Failed to connect to {host}")
    yield app


@pytest.fixture(scope="session")
def retailer_login():
    path = "retailer_context.json"
    response = requests.post(
        pytest.api + "/users/login",
        data={"email": pytest.retailer_username, "password": pytest.retailer_password},
    )
    token = response.json()["data"]["token"]
    json_dict = {
        "cookies": [],
        "origins": [
            {
                "origin": "https://dev.kingpin.global",
                "localStorage": [
                    {"name": "retailer_context", "value": ""},
                    {"name": "cRole", "value": "retailer"},
                    {"name": "cTok", "value": token},
                    {
                        "name": "userData",
                        "value": '{"ability":[{"action":"read","subject":"Dashboard"},{"action":"read","subject":"Order"},{"action":"read","subject":"Shipment"},{"action":"read","subject":"Transactions"},{"action":"read","subject":"Wallet"},{"action":"read","subject":"Profile"},{"action":"read","subject":"Referrals"},{"action":"read","subject":"Auth"},{"action":"read","subject":"Shop"},{"action":"read","subject":"Help"},{"action":"manage","subject":"Retailer"}]}',
                    },
                ],
            }
        ],
    }
    with open(path, "w") as outfile:
        json.dump(json_dict, outfile)
    yield
    os.remove(path)


@pytest.fixture(scope="session")
def brand_login():
    path = "brand_context.json"
    response = requests.post(
        pytest.api + "/users/login",
        data={"email": pytest.brand_username, "password": pytest.brand_password},
    )
    token = response.json()["data"]["token"]
    json_dict = {
        "cookies": [],
        "origins": [
            {
                "origin": "https://dev.kingpin.global",
                "localStorage": [
                    {"name": "brand_context", "value": ""},
                    {"name": "cRole", "value": "brand"},
                    {"name": "cTok", "value": token},
                    {
                        "name": "userData",
                        "value": '{"ability":[{"action":"read","subject":"Dashboard"},{"action":"read","subject":"Order"},{"action":"read","subject":"Shipment"},{"action":"read","subject":"Transactions"},{"action":"read","subject":"Wallet"},{"action":"read","subject":"Profile"},{"action":"read","subject":"Referrals"},{"action":"read","subject":"Auth"},{"action":"read","subject":"Shop"},{"action":"read","subject":"Help"},{"action":"manage","subject":"Brand"}]}',
                    },
                ],
            }
        ],
    }
    with open(path, "w") as outfile:
        json.dump(json_dict, outfile)
    yield
    os.remove(path)


@pytest.fixture(scope="session")
def retailer_login_ui(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(pytest.host)

    # Interact with login form
    page.locator('[name="login-email"]').fill(pytest.retailer_username)
    page.locator('[name="login-password"]').fill(pytest.retailer_password)
    page.locator('[type="submit"]').click()
    page.wait_for_load_state("networkidle")
    storage = context.storage_state(path="retailer_context.json")
    context.request.storage_state()
    context.close()


@pytest.fixture(scope="session")
def brand_login_ui(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(pytest.host)

    # Interact with login form
    page.locator('[name="login-email"]').fill(pytest.brand_username)
    page.locator('[name="login-password"]').fill(pytest.brand_password)
    page.locator('[type="submit"]').click()
    page.wait_for_load_state("networkidle")
    storage = context.storage_state(path="brand_context.json")
    context.close()


@pytest.fixture()
def login(page):
    page.goto("/login")
    log.info("Running fixture")
    # Interact with login form
    page.locator("[name='login-email']").fill(pytest.username)
    page.locator("[name='login-password']").fill(pytest.password)
    page.locator("[type='submit']").click()


@pytest.fixture(scope="session", autouse=True)
def browser_context(
    browser: Browser,
    browser_context_args: Dict,
    pytestconfig: Any,
    request: pytest.FixtureRequest,
    retailer_login,
    brand_login,
):
    pages: List[Page] = []
    retailer_context = browser.new_context(
        **browser_context_args, storage_state="retailer_context.json"
    )
    brand_context = browser.new_context(
        **browser_context_args, storage_state="brand_context.json"
    )
    contexts = [retailer_context, brand_context]
    Context = namedtuple("Context", "retailer_context, brand_context")
    tracing_option = pytestconfig.getoption("--tracing")
    capture_trace = tracing_option in ["on", "retain-on-failure"]
    for context in contexts:
        context.on("page", lambda page: pages.append(page))

        if capture_trace:
            context.tracing.start(
                name=slugify(request.node.nodeid),
                screenshots=True,
                snapshots=True,
                sources=True,
            )

    yield Context(retailer_context=retailer_context, brand_context=brand_context)

    # If request.node is missing rep_call, then some error happened during execution
    # that prevented teardown, but should still be counted as a failure
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else True

    if capture_trace:
        retain_trace = tracing_option == "on" or (
            failed and tracing_option == "retain-on-failure"
        )
        if retain_trace:
            trace_path = _build_artifact_test_folder(pytestconfig, request, "trace.zip")
            for context in contexts:
                context.tracing.stop(path=trace_path)
        else:
            for context in contexts:
                context.tracing.stop()

    screenshot_option = pytestconfig.getoption("--screenshot")
    capture_screenshot = screenshot_option == "on" or (
        failed and screenshot_option == "only-on-failure"
    )
    if capture_screenshot:
        for index, page in enumerate(pages):
            human_readable_status = "failed" if failed else "finished"
            screenshot_path = _build_artifact_test_folder(
                pytestconfig, request, f"test-{human_readable_status}-{index + 1}.png"
            )
            try:
                page.screenshot(timeout=5000, path=screenshot_path)
            except Error:
                pass
    for context in contexts:
        context.close()

    video_option = pytestconfig.getoption("--video")
    preserve_video = video_option == "on" or (
        failed and video_option == "retain-on-failure"
    )
    if preserve_video:
        for page in pages:
            video = page.video
            if not video:
                continue
            try:
                video_path = video.path()
                file_name = os.path.basename(video_path)
                video.save_as(
                    path=_build_artifact_test_folder(pytestconfig, request, file_name)
                )
            except Error:
                # Silent catch empty videos.
                pass


@pytest.fixture(scope="session")
def kingpin_db():
    client = MongoClient(MONGODB_CONNECTION_STRING)
    yield client.get_database("kingpin")
