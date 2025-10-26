"""Instagram Playwright helper reusing the Facebook session launcher."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from .facebook_playwright import open_session as facebook_open_session


@contextmanager
def open_session(start_url: str) -> Iterator[tuple]:
    with facebook_open_session(start_url) as session:
        yield session


__all__ = ["open_session"]
