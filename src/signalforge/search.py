"""Web search through the keyless DDGS metasearch adapter."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ddgs import DDGS
from ddgs.exceptions import DDGSException


@dataclass(frozen=True, slots=True)
class SearchResult:
    title: str
    url: str
    snippet: str


def search_web(query: str, max_results: int = 8) -> list[SearchResult]:
    """Return public web results. DDGS is a third-party metasearch, best-effort source."""
    if not query.strip():
        return []
    try:
        rows = DDGS().text(query, max_results=max_results)
    except DDGSException as exc:
        raise RuntimeError("Public search provider failed") from exc
    version_terms = re.findall(r"\b\d+(?:\.\d+){1,}\b", query)
    if version_terms:
        rows = [row for row in rows if all(
            version.lower() in f"{row.get('title', '')} {row.get('body', '')}".lower()
            for version in version_terms
        )]
    return [
        SearchResult(str(row.get("title", "")), str(row.get("href", "")), str(row.get("body", "")))
        for row in rows
        if row.get("href")
    ]
