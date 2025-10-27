"""Heuristic scoring rules for CMU relevance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class ScoredItem:
    text: str
    score: int
    label: str
    confidence: float
    notes: str


def _contains_any(text: str, terms: Iterable[str]) -> List[str]:
    lowered = text.lower()
    hits = []
    for term in terms:
        term_lower = term.lower().strip()
        if term_lower and term_lower in lowered:
            hits.append(term)
    return hits


def score_text(text: str, rules: Dict[str, Iterable[str]]) -> ScoredItem:
    """Apply CMU relevance rules and return a :class:`ScoredItem`."""

    content = text or ""
    positives = _contains_any(content, rules.get("positive_terms", []))
    negatives = _contains_any(content, rules.get("negative_terms", []))
    neutrals = _contains_any(content, rules.get("neutral_terms", []))

    score = len(positives) * 2 - len(negatives) * 2

    if score >= 2:
        label = "Colorado Mesa verified"
        confidence = 1.0
    elif score == 1:
        label = "Likely Colorado Mesa"
        confidence = 0.5
    elif score <= -2:
        label = "Not Colorado Mesa"
        confidence = 1.0
    else:
        label = "Uncertain"
        confidence = 0.3

    notes = [f"+{term}" for term in positives]
    notes.extend(f"-{term}" for term in negatives)
    notes.extend(f"~{term}" for term in neutrals)

    return ScoredItem(
        text=content,
        score=score,
        label=label,
        confidence=confidence,
        notes=";".join(notes),
    )


__all__ = ["ScoredItem", "score_text"]
