"""公共 fixture、页面对象注入与失败截图。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

ROOT = Path(__file__).resolve().parent
SCREENSHOT_DIR = ROOT / "reports" / "screenshots"


def _load_users() -> dict:
    return json.loads((ROOT / "data" / "users.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def users() -> dict:
    return _load_users()


@pytest.fixture(scope="session")
def base_url(users: dict) -> str:
    return users["base_url"]


@pytest.fixture
def login_page(page: Page, base_url: str) -> LoginPage:
    return LoginPage(page, base_url)


@pytest.fixture
def inventory_page(page: Page, base_url: str) -> InventoryPage:
    return InventoryPage(page, base_url)


@pytest.fixture
def cart_page(page: Page, base_url: str) -> CartPage:
    return CartPage(page, base_url)


@pytest.fixture
def checkout_page(page: Page, base_url: str) -> CheckoutPage:
    return CheckoutPage(page, base_url)


@pytest.fixture
def logged_in_inventory(login_page: LoginPage, users: dict) -> InventoryPage:
    """用标准用户登录后停在商品列表页，供购物车与结算用例复用。"""
    account = users["standard"]
    login_page.open().login(account["username"], account["password"])
    return InventoryPage(login_page.page, login_page.base_url)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """用例失败时自动截图，并把路径写进测试报告。"""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    screenshot = SCREENSHOT_DIR / f"{item.name}.png"
    try:
        page.screenshot(path=str(screenshot), full_page=True)
    except Exception:
        return
    report.sections.append(("失败截图", str(screenshot)))
