"""Single-round bounded research workflow."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter
from uuid import uuid4

from signalforge.evidence import Evidence, deduplicate, make_evidence
from signalforge.fetch import FetchError, fetch_text
from signalforge.observability import operation_span, workflow_span
from signalforge.report import write_report
from signalforge.search import SearchResult, search_web
from signalforge.state import save_evidence
from signalforge.verify import verify_evidence


def _run_research(question: str, output: Path, max_sources: int = 8,
                  urls: list[str] | None = None) -> tuple[list[Evidence], Path, Path]:
    started = perf_counter()
    run_id = uuid4().hex
    results = [SearchResult("User-provided source", url, "") for url in (urls or [])]
    search_provider = "user_urls" if results else "ddgs"
    if not results:
        with operation_span("web_search"):
            results = search_web(question, max_results=max_sources)
    results = deduplicate(results)[:max_sources]
    evidence: list[Evidence] = []
    retries = 0
    failures = 0
    for result in results:
        text = ""
        for attempt in range(2):
            try:
                with operation_span("fetch_source"):
                    text = fetch_text(result.url)
                break
            except FetchError:
                if attempt == 0:
                    retries += 1
                else:
                    failures += 1
            except (ValueError, OSError):
                failures += 1
                break
        if not text:
            continue
        evidence.append(make_evidence(result, text, query=question))
    evidence.sort(key=lambda item: (item.source_type == "primary", item.evidence_strength == "strong"), reverse=True)
    findings = verify_evidence(evidence)
    output.mkdir(parents=True, exist_ok=True)
    save_evidence(output / "state.json", evidence)
    metadata = {
        "run_id": run_id,
        "question": question,
        "search_provider": search_provider,
        "model_provider": None,
        "sources_found": len(results),
        "sources_captured": len(evidence),
        "retries": retries,
        "failures": failures,
        "elapsed_seconds": round(perf_counter() - started, 3),
        "token_usage": None,
        "cost": None,
    }
    report, ledger = write_report(question, evidence, findings, output, metadata)
    return evidence, report, ledger


def run_research(question: str, output: Path, max_sources: int = 8,
                 urls: list[str] | None = None) -> tuple[list[Evidence], Path, Path]:
    with workflow_span():
        return _run_research(question, output, max_sources, urls)
