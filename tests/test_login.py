"""登录功能测试：正常登录、账号锁定、错误密码、必填校验、退出登录。"""

from __future__ import annotations

import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage


@pytest.mark.ui
@pytest.mark.smoke
def test_standard_user_can_login(login_page, users, page):
    account = users["standard"]
    login_page.open().login(account["username"], account["password"])

    expect(page).to_have_url(f"{login_page.base_url}/inventory.html")
    assert InventoryPage(page, login_page.base_url).item_count() == 6


@pytest.mark.ui
def test_locked_out_user_is_rejected(login_page, users):
    account = users["locked_out"]
    login_page.open().login(account["username"], account["password"])

    assert "locked out" in login_page.error_text()
    login_page.expect_url()


@pytest.mark.ui
def test_wrong_password_shows_credential_error(login_page, users):
    account = users["invalid_password"]
    login_page.open().login(account["username"], account["password"])

    assert "Username and password do not match" in login_page.error_text()


@pytest.mark.ui
@pytest.mark.regression
def test_empty_username_shows_required_error(login_page, users):
    account = users["standard"]
    login_page.open()
    login_page.fill_password(account["password"])
    login_page.submit()

    assert "Username is required" in login_page.error_text()


@pytest.mark.ui
@pytest.mark.regression
def test_empty_password_shows_required_error(login_page, users):
    account = users["standard"]
    login_page.open()
    login_page.fill_username(account["username"])
    login_page.submit()

    assert "Password is required" in login_page.error_text()


@pytest.mark.ui
def test_logout_returns_to_login_page(logged_in_inventory):
    inventory = logged_in_inventory
    inventory.logout()

    expect(inventory.page).to_have_url(f"{inventory.base_url}/")
    expect(inventory.page.locator("#login-button")).to_be_visible()
