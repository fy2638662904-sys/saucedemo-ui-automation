"""SauceDemo 结算流程页（信息填写 + 订单完成）。"""

from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    PATH = "/checkout-step-one.html"

    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    POSTAL_CODE_INPUT = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    FINISH_BUTTON = "#finish"
    ERROR_MESSAGE = "[data-test='error']"
    COMPLETE_HEADER = "[data-test='complete-header']"
    SUMMARY_TOTAL = "[data-test='total-label']"

    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.page.fill(self.FIRST_NAME_INPUT, first_name)
        self.page.fill(self.LAST_NAME_INPUT, last_name)
        if postal_code:
            self.page.fill(self.POSTAL_CODE_INPUT, postal_code)

    def continue_to_summary(self) -> None:
        self.page.click(self.CONTINUE_BUTTON)

    def finish(self) -> None:
        self.page.click(self.FINISH_BUTTON)

    @property
    def error(self):
        return self.page.locator(self.ERROR_MESSAGE)

    def error_text(self) -> str:
        expect(self.error).to_be_visible()
        return self.error.inner_text()

    def complete_text(self) -> str:
        expect(self.page.locator(self.COMPLETE_HEADER)).to_be_visible()
        return self.page.locator(self.COMPLETE_HEADER).inner_text()

    def order_total(self) -> str:
        expect(self.page.locator(self.SUMMARY_TOTAL)).to_be_visible()
        return self.page.locator(self.SUMMARY_TOTAL).inner_text()
