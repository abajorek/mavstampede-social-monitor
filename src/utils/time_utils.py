"""Time-related helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import re
from typing import Tuple

Window = Tuple[datetime, datetime]


def parse_window(window_str: str, *, now: datetime | None = None) -> Window:
    """Parse ``<number><unit>`` windows such as ``"21d"``.

    Supported units:
    - ``d`` – days
    - ``w`` – weeks
    - ``h`` – hours
    """

    if now is None:
        now = datetime.now(timezone.utc)

    match = re.fullmatch(r"(\d+)([dwh])", window_str.strip())
    if not match:
        return now - timedelta(days=21), now

    value = int(match.group(1))
    unit = match.group(2)

    delta_map = {
        "d": timedelta(days=value),
        "w": timedelta(weeks=value),
        "h": timedelta(hours=value),
    }

    return now - delta_map[unit], now


__all__ = ["parse_window", "Window"]
