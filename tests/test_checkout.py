"""结算流程测试：完整下单链路与必填项校验。"""

from __future__ import annotations

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

BACKPACK = "Sauce Labs Backpack"


@pytest.mark.ui
@pytest.mark.smoke
def test_end_to_end_checkout_success(logged_in_inventory):
    inventory = logged_in_inventory
    inventory.add_to_cart(BACKPACK)
    inventory.open_cart()

    cart = CartPage(inventory.page, inventory.base_url)
    cart.checkout()

    checkout = CheckoutPage(inventory.page, inventory.base_url)
    checkout.fill_info("Test", "User", "200000")
    checkout.continue_to_summary()

    assert "$" in checkout.order_total()

    checkout.finish()
    assert "Thank you for your order" in checkout.complete_text()


@pytest.mark.ui
@pytest.mark.regression
def test_checkout_requires_postal_code(logged_in_inventory):
    inventory = logged_in_inventory
    inventory.add_to_cart(BACKPACK)
    inventory.open_cart()

    CartPage(inventory.page, inventory.base_url).checkout()

    checkout = CheckoutPage(inventory.page, inventory.base_url)
    checkout.fill_info("Test", "User", "")
    checkout.continue_to_summary()

    assert "Postal Code is required" in checkout.error_text()
