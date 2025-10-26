"""Thin Playwright helper to open a manual browser session."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from playwright.sync_api import sync_playwright


@contextmanager
def open_session(start_url: str) -> Iterator[tuple]:
    """Launch Chromium and yield (browser, context, page).

    The caller is responsible for closing the browser. This helper is purposely
    minimal and expects the human operator to perform any authentication.
    """

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(start_url)
        print("Complete login and press ENTER to continue...")
        input()
        try:
            yield browser, context, page
        finally:
            page.close()
            context.close()
            browser.close()


__all__ = ["open_session"]
