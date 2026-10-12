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


def test_primary_source_detection_and_quantitative_preference():
    primary_url = "https://arxiv.org/abs/2603.99999"
    paper_text = (
        "Abstract: In this paper we propose a novel approach for JIT compiler optimization.\n\n"
        "Benchmark Evaluation: Across 45 distinct pyperformance benchmarks, the tier-2 interpreter "
        "achieved an average 18.2% faster execution time with 5% lower memory overhead on 2026-03-15."
    )
    # Verifies primary paper selects quantitative benchmark results over abstract alone
    excerpt = select_excerpt(paper_text, "JIT compiler optimization", is_primary=True)
    assert "18.2% faster" in excerpt
    assert "Abstract:" not in excerpt

    row = SearchResult("JIT Paper", primary_url, "Abstract snippet")
    ev = make_evidence(row, paper_text, query="JIT compiler optimization")
    assert ev.source_type == "primary"
    assert ev.measured_outcome is not None and "18.2% faster" in ev.measured_outcome
    assert ev.methodology == "Empirical benchmark evaluation"
    assert ev.sample_size is not None and "45" in ev.sample_size
    assert ev.evidence_strength == "strong"
    assert ev.publication_date == "2026-03-15"


def test_missing_quantitative_details_flags_limitation():
    blog_url = "https://techblog.example.com/jit-review"
    vague_text = (
        "The new runtime is significantly faster and feels much smoother than before, "
        "providing a great experience for everyday users without any noticeable delays."
    )
    row = SearchResult("Blog Review", blog_url, "Snippet")
    ev = make_evidence(row, vague_text, query="faster runtime")
    assert ev.source_type == "secondary"
    assert ev.measured_outcome is None
    assert ev.sample_size is None
    assert "Missing quantitative details or sample size" in ev.limitations
    assert ev.evidence_strength in ("weak", "moderate")
