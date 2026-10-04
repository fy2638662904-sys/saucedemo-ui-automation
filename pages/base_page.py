"""页面对象基类：统一 URL 拼接与常用等待。"""

from __future__ import annotations

from playwright.sync_api import Page, expect


class BasePage:
    PATH = "/"

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    @property
    def url(self) -> str:
        return f"{self.base_url}{self.PATH}"

    def open(self) -> "BasePage":
        self.page.goto(self.url)
        self.wait_loaded()
        return self

    def wait_loaded(self) -> None:
        self.page.wait_for_load_state("domcontentloaded")

    def expect_url(self) -> None:
        expect(self.page).to_have_url(self.url)

    def title(self) -> str:
        return self.page.title()
