"""商品列表页测试：商品数量、价格排序、名称排序、加购状态。"""

from __future__ import annotations

import pytest


@pytest.mark.ui
@pytest.mark.smoke
def test_inventory_shows_six_items(logged_in_inventory):
    inventory = logged_in_inventory

    assert inventory.item_count() == 6
    assert len(inventory.item_prices()) == 6


@pytest.mark.ui
def test_sort_by_price_low_to_high(logged_in_inventory):
    inventory = logged_in_inventory
    inventory.sort_by("lohi")

    prices = inventory.item_prices()
    assert prices == sorted(prices)
    assert inventory.item_names()[0] == "Sauce Labs Onesie"


@pytest.mark.ui
def test_sort_by_name_descending(logged_in_inventory):
    inventory = logged_in_inventory
    inventory.sort_by("za")

    names = inventory.item_names()
    assert names == sorted(names, reverse=True)
    assert names[0] == "Test.allTheThings() T-Shirt (Red)"
