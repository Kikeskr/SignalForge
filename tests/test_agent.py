import json

from signalforge.agent import run_research
from signalforge.search import SearchResult


def test_workflow_continues_after_one_source_failure(monkeypatch, tmp_path):
    monkeypatch.setattr("signalforge.agent.search_web", lambda *a, **k: [
        SearchResult("bad", "https://bad.example", ""),
        SearchResult("good", "https://good.example", ""),
    ])

    def fetch(url):
        if "bad" in url:
            raise ValueError("invalid")
        return "This is a sufficiently long source paragraph about the example research question."

    monkeypatch.setattr("signalforge.agent.fetch_text", fetch)
    evidence, report, ledger = run_research("example research question", tmp_path)
    assert len(evidence) == 1
    assert report.exists() and ledger.exists() and (tmp_path / "run.json").exists()
    saved = json.loads(ledger.read_text(encoding="utf-8"))
    assert saved["sources"][0]["evidence_id"] == evidence[0].evidence_id
    metadata = json.loads((tmp_path / "run.json").read_text(encoding="utf-8"))
    assert metadata["sources_captured"] == 1


def test_bounded_fetch_retry(monkeypatch, tmp_path):
    calls = 0

    def search(*a, **k):
        return [SearchResult("ok", "https://example.org", "")]

    def fetch(url):
        nonlocal calls
        calls += 1
        if calls == 1:
            from signalforge.fetch import FetchError

            raise FetchError("temporary")
        return "This is a sufficiently long source paragraph about recovery behavior."

    monkeypatch.setattr("signalforge.agent.search_web", search)
    monkeypatch.setattr("signalforge.agent.fetch_text", fetch)
    evidence, _, _ = run_research("recovery behavior", tmp_path)
    assert len(evidence) == 1
    assert calls == 2
