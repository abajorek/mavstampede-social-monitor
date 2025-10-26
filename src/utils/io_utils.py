"""Utility helpers for reading CSV inputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_csvs(in_dir: Path | str, pattern: str = "*.csv") -> pd.DataFrame:
    """Load and concatenate CSV files from ``in_dir``.

    Parameters
    ----------
    in_dir:
        Directory containing the CSV files.
    pattern:
        Glob pattern to match files. Defaults to ``"*.csv"``.

    Returns
    -------
    pandas.DataFrame
        Combined frame with an additional ``__source_file`` column so that the
        origin of each row is visible downstream. If no files are found, an
        empty DataFrame is returned.
    """

    base_path = Path(in_dir)
    frames: list[pd.DataFrame] = []

    if not base_path.exists():
        return pd.DataFrame()

    for csv_path in sorted(base_path.glob(pattern)):
        if not csv_path.is_file():
            continue

        try:
            df = pd.read_csv(csv_path)
        except Exception as exc:  # pragma: no cover - defensive logging
            print(f"Failed to read {csv_path}: {exc}")
            continue

        df["__source_file"] = csv_path.name
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


__all__ = ["read_csvs"]
