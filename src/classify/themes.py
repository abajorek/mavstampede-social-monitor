"""Keyword driven theme tagging."""

from __future__ import annotations

from typing import List

THEMES: list[str] = [
    "sound",
    "drill",
    "uniforms",
    "spirit",
    "shout-outs",
    "logistics",
]

_THEME_KEYWORDS: dict[str, tuple[str, ...]] = {
    "sound": ("sound", "loud", "mix", "audio", "drumline", "battery", "pit"),
    "drill": ("drill", "set", "forms", "formation", "charts", "pyware"),
    "uniforms": ("uniform", "plume", "gauntlet", "shako", "hat"),
    "spirit": ("go mavs", "go mavericks", "spirit", "hype", "fight song", "crowd"),
    "shout-outs": ("shout out", "shout-out", "props", "great job", "thank", "proud"),
    "logistics": ("arrival", "parking", "gate", "schedule", "time", "logistics"),
}


def guess_themes(text: str) -> List[str]:
    """Return a list of theme labels based on keyword matches."""

    lowered = (text or "").lower()
    matches: list[str] = []
    for theme, keywords in _THEME_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            matches.append(theme)

    return matches or ["shout-outs"]


__all__ = ["THEMES", "guess_themes"]
