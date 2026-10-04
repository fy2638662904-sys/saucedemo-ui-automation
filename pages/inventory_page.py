"""SauceDemo 商品列表页。"""

from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class InventoryPage(BasePage):
    PATH = "/inventory.html"

    ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    SORT_SELECT = "[data-test='product-sort-container']"
    CART_LINK = "[data-test='shopping-cart-link']"
    CART_BADGE = "[data-test='shopping-cart-badge']"
    MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def is_loaded(self) -> bool:
        return self.page.url.endswith(self.PATH)

    def item_count(self) -> int:
        expect(self.page.locator(self.ITEM).first).to_be_visible()
        return self.page.locator(self.ITEM).count()

    def item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def item_prices(self) -> list[float]:
        texts = self.page.locator(self.ITEM_PRICE).all_inner_texts()
        return [float(text.replace("$", "")) for text in texts]

    def sort_by(self, value: str) -> None:
        """value 取值：az / za / lohi / hilo。"""
        self.page.select_option(self.SORT_SELECT, value)

    def add_to_cart(self, item_name: str) -> None:
        self._item_card(item_name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, item_name: str) -> None:
        self._item_card(item_name).get_by_role("button", name="Remove").click()

    def cart_badge_count(self) -> int:
        badge = self.page.locator(self.CART_BADGE)
        if badge.count() == 0:
            return 0
        return int(badge.inner_text())

    def open_cart(self) -> None:
        self.page.click(self.CART_LINK)

    def logout(self) -> None:
        self.page.click(self.MENU_BUTTON)
        self.page.click(self.LOGOUT_LINK)

    def _item_card(self, item_name: str):
        card = self.page.locator(self.ITEM).filter(has_text=item_name)
        expect(card).to_have_count(1)
        return card
