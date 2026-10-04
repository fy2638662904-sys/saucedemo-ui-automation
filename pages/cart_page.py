"""SauceDemo 购物车页。"""

from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class CartPage(BasePage):
    PATH = "/cart.html"

    CART_ITEM = ".cart_item"
    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING = "#continue-shopping"

    def item_names(self) -> list[str]:
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def item_count(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    def remove(self, item_name: str) -> None:
        card = self.page.locator(self.CART_ITEM).filter(has_text=item_name)
        expect(card).to_have_count(1)
        card.get_by_role("button", name="Remove").click()

    def checkout(self) -> None:
        self.page.click(self.CHECKOUT_BUTTON)
