"""Evidence capture and stable source deduplication."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import UTC, datetime

from signalforge.fetch import canonicalize_url
from signalforge.search import SearchResult


@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: str
    title: str
    url: str
    retrieved_at: str
    excerpt: str
    publication_date: str | None = None


def make_evidence(result: SearchResult, text: str, retrieved_at: str | None = None,
                  query: str = "") -> Evidence:
    url = canonicalize_url(result.url)
    evidence_id = "E-" + hashlib.sha256(url.encode()).hexdigest()[:10].upper()
    excerpt = (select_excerpt(text, query) or result.snippet).strip()[:1200]
    return Evidence(evidence_id, result.title.strip() or url, url,
                    retrieved_at or datetime.now(UTC).isoformat(), excerpt)


def select_excerpt(text: str, query: str) -> str:
    """Pick a bounded paragraph with useful query-term overlap."""
    chunks = [re.sub(r"\s+", " ", part).strip() for part in re.split(r"\n+|(?<=[.!?])\s+", text)]
    chunks = [part for part in chunks if len(part) >= 60]
    terms = {word.lower() for word in re.findall(r"\d+(?:\.\d+)+|[a-zA-Z][\w'-]{2,}", query)}
    if not chunks:
        return text.strip()[:1200]
    return max(chunks, key=lambda part: sum(word in part.lower() for word in terms))[:1200]


def deduplicate(results: list[SearchResult]) -> list[SearchResult]:
    seen: set[str] = set()
    unique: list[SearchResult] = []
    for result in results:
        try:
            url = canonicalize_url(result.url)
        except ValueError:
            continue
        if url not in seen:
            seen.add(url)
            unique.append(SearchResult(result.title, url, result.snippet))
    return unique
