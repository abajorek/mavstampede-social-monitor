"""Very small helper for running Google search queries."""

from __future__ import annotations

import random
import time
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )
}


def google_search(query: str, *, tbs: str | None = None, pause: tuple[float, float] = (3, 6)) -> list[dict[str, str]]:
    """Perform a lightweight Google search and parse the first page of results."""

    url = f"https://www.google.com/search?q={quote_plus(query)}"
    if tbs:
        url += f"&tbs={tbs}"

    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    time.sleep(random.uniform(*pause))

    soup = BeautifulSoup(response.text, "html.parser")
    results: list[dict[str, str]] = []

    for result in soup.select("div.g"):
        anchor = result.select_one("a")
        if not anchor or not anchor.get("href"):
            continue
        title = anchor.get_text(strip=True)
        link = anchor["href"]
        results.append({"title": title, "url": link})

    return results


__all__ = ["google_search", "HEADERS"]
