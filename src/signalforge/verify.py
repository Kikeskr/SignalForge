"""Conservative reference and contradiction checks for source excerpts."""

from __future__ import annotations

import re
from dataclasses import dataclass

from signalforge.evidence import Evidence

OPPOSITES = ({"increased", "rose", "grew", "higher", "more"}, {"decreased", "fell", "shrank", "lower", "less"})


@dataclass(frozen=True, slots=True)
class Finding:
    text: str
    evidence_ids: tuple[str, ...]
    status: str


def verify_evidence(evidence: list[Evidence]) -> list[Finding]:
    findings = [Finding(item.excerpt, (item.evidence_id,), "partially_supported") for item in evidence if item.excerpt]
    known = {item.evidence_id for item in evidence}
    findings = [f for f in findings if all(ref in known for ref in f.evidence_ids)]
    for i, first in enumerate(findings):
        a = set(re.findall(r"[a-z]{4,}", first.text.lower()))
        for second in findings[i + 1:]:
            b = set(re.findall(r"[a-z]{4,}", second.text.lower()))
            if len(a & b) < 4:
                continue
            if any((a & left and b & right) or (a & right and b & left) for left, right in [OPPOSITES]):
                findings[i] = Finding(first.text, first.evidence_ids, "conflicted")
                idx = findings.index(second)
                findings[idx] = Finding(second.text, second.evidence_ids, "conflicted")
    return findings


def validate_references(findings: list[Finding], evidence: list[Evidence]) -> bool:
    known = {item.evidence_id for item in evidence}
    return all(ref in known for finding in findings for ref in finding.evidence_ids)
