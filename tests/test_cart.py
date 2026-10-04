"""购物车测试：加入商品、徽标计数、移除商品、购物车内容。"""

from __future__ import annotations

import pytest

from pages.cart_page import CartPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.ui
@pytest.mark.smoke
def test_add_single_item_updates_badge(logged_in_inventory):
    inventory = logged_in_inventory
    assert inventory.cart_badge_count() == 0

    inventory.add_to_cart(BACKPACK)

    assert inventory.cart_badge_count() == 1


@pytest.mark.ui
def test_add_two_items_and_remove_one(logged_in_inventory):
    inventory = logged_in_inventory
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    assert inventory.cart_badge_count() == 2

    inventory.remove_from_cart(BACKPACK)

    assert inventory.cart_badge_count() == 1


@pytest.mark.ui
def test_cart_page_lists_added_item(logged_in_inventory):
    inventory = logged_in_inventory
    inventory.add_to_cart(BACKPACK)
    inventory.open_cart()

    cart = CartPage(inventory.page, inventory.base_url)
    cart.expect_url()
    assert cart.item_count() == 1
    assert cart.item_names() == [BACKPACK]


@pytest.mark.ui
@pytest.mark.regression
def test_remove_item_from_cart_page_clears_badge(logged_in_inventory):
    inventory = logged_in_inventory
    inventory.add_to_cart(BACKPACK)
    inventory.open_cart()

    cart = CartPage(inventory.page, inventory.base_url)
    cart.remove(BACKPACK)

    assert cart.item_count() == 0
    assert inventory.cart_badge_count() == 0
