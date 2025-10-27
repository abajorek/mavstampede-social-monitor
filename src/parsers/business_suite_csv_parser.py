"""Utilities for normalizing Business Suite style CSV exports."""

from __future__ import annotations

import pandas as pd


def _column(df: pd.DataFrame, names: list[str] | tuple[str, ...], default: str = "") -> pd.Series:
    for name in names:
        if name in df.columns:
            return df[name]
        lowered = name.lower()
        for column in df.columns:
            if column.lower() == lowered:
                return df[column]
    return pd.Series([default] * len(df))


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """Return a normalized dataframe with consistent column names."""

    if df.empty:
        return pd.DataFrame(
            columns=[
                "date_utc",
                "platform",
                "post_url",
                "post_owner_handle",
                "post_caption_excerpt",
                "comment_id",
                "commenter_handle",
                "comment_text",
            ]
        )

    normalized = pd.DataFrame(
        {
            "date_utc": _column(df, ["date", "timestamp", "created_at"]),
            "platform": _column(df, ["platform"], default="facebook"),
            "post_url": _column(df, ["post_url", "url", "link"]),
            "post_owner_handle": _column(df, ["post_owner", "page", "owner"]),
            "post_caption_excerpt": _column(df, ["post_caption", "caption", "message"]),
            "comment_id": _column(df, ["comment_id", "cid", "commentid"]),
            "commenter_handle": _column(df, ["commenter", "user", "username", "profile_name"]),
            "comment_text": _column(df, ["comment_text", "text", "message", "body"]),
        }
    )

    normalized["post_caption_excerpt"] = (
        normalized["post_caption_excerpt"].astype(str).str.slice(0, 200)
    )

    return normalized


__all__ = ["normalize_df"]
