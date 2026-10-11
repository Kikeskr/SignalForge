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
