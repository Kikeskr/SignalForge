from signalforge.evidence import Evidence
from signalforge.state import load_evidence, save_evidence


def test_evidence_state_round_trip(tmp_path):
    records = [Evidence("E-ABC", "Example", "https://example.org", "2026-01-01", "excerpt")]
    path = tmp_path / "state.json"
    save_evidence(path, records)
    assert load_evidence(path) == records
