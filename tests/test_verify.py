from signalforge.evidence import Evidence
from signalforge.verify import Finding, validate_references, verify_evidence


def test_invalid_reference_is_detected():
    assert not validate_references([Finding("claim", ("missing",), "supported")], [])


def test_opposing_statements_marked_conflicted():
    rows = [
        Evidence("E-A", "a", "https://a.example", "now", "The adoption of widgets increased rapidly in the last year."),
        Evidence("E-B", "b", "https://b.example", "now", "The adoption of widgets decreased rapidly in the last year."),
    ]
    results = verify_evidence(rows)
    assert [item.status for item in results] == ["conflicted", "conflicted"]


def test_unreviewed_excerpt_is_not_claimed_fully_verified():
    row = Evidence("E-A", "a", "https://a.example", "now", "A source excerpt.")
    assert verify_evidence([row])[0].status == "partially_supported"


def test_explicit_uncertainty_is_marked_uncertain():
    row = Evidence(
        evidence_id="E-U",
        title="Preliminary Study",
        url="https://example.org/study",
        retrieved_at="2026-10-12T00:00:00Z",
        excerpt="The preliminary benchmark findings remain inconclusive and uncertain regarding real-world throughput.",
    )
    results = verify_evidence([row])
    assert len(results) == 1
    assert results[0].status == "uncertain"
    assert results[0].evidence_strength == "weak"
    assert results[0].is_attributed_only is True


def test_secondary_repetition_does_not_mark_claim_independently_verified():
    # Multiple secondary news sources repeating the same claim must NOT be marked verified_independent
    r1 = Evidence(
        "E-1", "News 1", "https://news1.example.com/python", "now",
        "Python 3.12 delivers 15% faster execution on standard suites.",
        source_type="secondary", measured_outcome="15% faster execution"
    )
    r2 = Evidence(
        "E-2", "News 2", "https://news2.example.com/python", "now",
        "Python 3.12 delivers 15% faster execution on standard suites.",
        source_type="secondary", measured_outcome="15% faster execution"
    )
    r3 = Evidence(
        "E-3", "News 3", "https://news3.example.com/python", "now",
        "Python 3.12 delivers 15% faster execution on standard suites.",
        source_type="secondary", measured_outcome="15% faster execution"
    )
    results = verify_evidence([r1, r2, r3])
    for item in results:
        assert item.status == "partially_supported"
        assert item.is_attributed_only is True
        assert item.status != "verified_independent"


def test_independent_primary_sources_elevate_to_verified_independent():
    # Two distinct primary empirical sources independently measuring and confirming the claim
    p1 = Evidence(
        "E-P1", "PEP 709", "https://peps.python.org/pep-0709/", "now",
        "Inlined comprehensions deliver 12% faster execution on pyperformance.",
        source_type="primary", measured_outcome="12% faster execution", evidence_strength="strong"
    )
    p2 = Evidence(
        "E-P2", "ArXiv Paper", "https://arxiv.org/abs/2604.12345", "now",
        "Independent measurement confirms comprehensions deliver 12% faster execution on pyperformance.",
        source_type="primary", measured_outcome="12% faster execution", evidence_strength="strong"
    )
    results = verify_evidence([p1, p2])
    assert any(item.status == "verified_independent" and item.is_attributed_only is False for item in results)
