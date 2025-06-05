"""Simple keyword tagging utilities."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, Iterable, List

try:
    import yake  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yake = None  # type: ignore


# Basic English stop words used when YAKE is unavailable
_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
}


def _extract_with_yake(text: str, top_k: int) -> List[str]:
    """Extract keywords from ``text`` using YAKE if available."""

    if not yake:
        return []
    kw_extractor = yake.KeywordExtractor(lan="en", n=1, top=top_k * 2)
    keywords = kw_extractor.extract_keywords(text)
    tags: List[str] = []
    for kw, _score in keywords:
        kw = kw.lower().strip()
        if kw not in tags:
            tags.append(kw)
        if len(tags) >= top_k:
            break
    return tags


def _extract_simple(text: str, top_k: int) -> List[str]:
    """Fallback keyword extraction using word frequency."""

    tokens = re.findall(r"[a-zA-Z0-9']+", text.lower())
    tokens = [t for t in tokens if t not in _STOP_WORDS and len(t) > 2]
    counts = Counter(tokens)
    tags: List[str] = []
    for word, _ in counts.most_common():
        if word not in tags:
            tags.append(word)
        if len(tags) >= top_k:
            break
    return tags


def extract_tags(name: str | None, description: str | None, top_k: int = 5) -> List[str]:
    """Return up to ``top_k`` keyword tags for a record."""

    text_parts = [name or "", description or ""]
    text = " ".join(part for part in text_parts if part).strip()
    if not text:
        return []

    tags = _extract_with_yake(text, top_k)
    if not tags:
        tags = _extract_simple(text, top_k)
    return tags


def tag_records(records: Iterable[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
    """Add keyword tags to each record in ``records``."""

    tagged: List[Dict[str, Any]] = []
    for rec in records:
        name = rec.get("name")
        desc = rec.get("description")
        rec_tags = extract_tags(name, desc, top_k)
        rec = {**rec, "tags": rec_tags}
        tagged.append(rec)
    return tagged
