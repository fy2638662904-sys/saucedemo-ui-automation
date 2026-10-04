"""SauceDemo 登录页。"""

from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/"

    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def login(self, username: str, password: str) -> None:
        self.fill_username(username)
        self.fill_password(password)
        self.submit()

    def fill_username(self, username: str) -> None:
        self.page.fill(self.USERNAME_INPUT, username)

    def fill_password(self, password: str) -> None:
        self.page.fill(self.PASSWORD_INPUT, password)

    def submit(self) -> None:
        self.page.click(self.LOGIN_BUTTON)

    @property
    def error(self):
        return self.page.locator(self.ERROR_MESSAGE)

    def error_text(self) -> str:
        expect(self.error).to_be_visible()
        return self.error.inner_text()
