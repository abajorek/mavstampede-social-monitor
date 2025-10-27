"""Output helpers."""

from __future__ import annotations

import pandas as pd


def save_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)


__all__ = ["save_csv"]
