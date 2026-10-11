from signalforge.evidence import deduplicate, make_evidence, select_excerpt
from signalforge.search import SearchResult


def test_deduplicate_normalized_urls():
    rows = [SearchResult("a", "https://example.org/?utm_source=x", "one"),
            SearchResult("b", "https://example.org/", "two")]
    assert len(deduplicate(rows)) == 1


def test_evidence_id_is_stable_and_excerpt_bounded():
    row = SearchResult("title", "https://example.org", "")
    assert make_evidence(row, "body", "2026-01-01").evidence_id == make_evidence(row, "other", "later").evidence_id
    assert len(make_evidence(row, "x" * 2000).excerpt) == 1200


def test_excerpt_prefers_most_relevant_paragraph():
    text = "Unrelated overview paragraph with enough words to pass the normal length filter.\n"
    text += "Python 3.12.10 fixes a notable security issue and improves build reliability."
    assert "3.12.10" in select_excerpt(text, "Python 3.12.10 security fixes")
