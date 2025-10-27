"""Simple sentiment helper built on top of CMU scores."""

from __future__ import annotations


def sentiment_from_score(score: int) -> str:
    if score >= 2:
        return "positive"
    if score <= -2:
        return "negative"
    return "neutral"


__all__ = ["sentiment_from_score"]
