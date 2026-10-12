"""Conservative reference, attribution, and contradiction checks for source excerpts."""

from __future__ import annotations

import re
from dataclasses import dataclass

from signalforge.evidence import Evidence, detect_uncertainty

OPPOSITES = (
    {"increased", "rose", "grew", "higher", "more", "faster", "improved", "boosted", "speedup"},
    {"decreased", "fell", "shrank", "lower", "less", "slower", "worsened", "dropped", "slowdown"},
)


@dataclass(frozen=True, slots=True)
class Finding:
    text: str
    evidence_ids: tuple[str, ...]
    status: str
    source_type: str = "secondary"
    publication_date: str | None = None
    sample_size: str | None = None
    methodology: str | None = None
    measured_outcome: str | None = None
    supporting_excerpt: str = ""
    limitations: tuple[str, ...] = ()
    evidence_strength: str = "moderate"
    is_attributed_only: bool = True
    claim_text: str = ""

    def __post_init__(self) -> None:
        if isinstance(self.limitations, list):
            object.__setattr__(self, "limitations", tuple(self.limitations))
        if isinstance(self.evidence_ids, list):
            object.__setattr__(self, "evidence_ids", tuple(self.evidence_ids))
        if not self.claim_text:
            object.__setattr__(self, "claim_text", self.text)
        if not self.supporting_excerpt:
            object.__setattr__(self, "supporting_excerpt", self.text)


def verify_evidence(evidence: list[Evidence]) -> list[Finding]:
    findings: list[Finding] = []
    evidence_by_id = {item.evidence_id: item for item in evidence}

    for item in evidence:
        if not item.excerpt:
            continue
        is_uncertain = detect_uncertainty(item.excerpt)
        if is_uncertain:
            status = "uncertain"
            strength = "weak"
        else:
            status = "partially_supported"
            strength = item.evidence_strength

        findings.append(
            Finding(
                text=item.excerpt,
                evidence_ids=(item.evidence_id,),
                status=status,
                source_type=item.source_type,
                publication_date=item.publication_date,
                sample_size=item.sample_size,
                methodology=item.methodology,
                measured_outcome=item.measured_outcome,
                supporting_excerpt=item.excerpt,
                limitations=item.limitations,
                evidence_strength=strength,
                is_attributed_only=True,
                claim_text=item.excerpt,
            )
        )

    # Contradiction / Conflict detection
    for i, first in enumerate(findings):
        a = set(re.findall(r"[a-z]{4,}", first.text.lower()))
        for second in findings[i + 1:]:
            b = set(re.findall(r"[a-z]{4,}", second.text.lower()))
            if len(a & b) < 4:
                continue
            is_conflicted = any(
                (a & left and b & right) or (a & right and b & left)
                for left, right in [OPPOSITES]
            )
            if is_conflicted:
                findings[i] = Finding(
                    text=first.text,
                    evidence_ids=first.evidence_ids,
                    status="conflicted",
                    source_type=first.source_type,
                    publication_date=first.publication_date,
                    sample_size=first.sample_size,
                    methodology=first.methodology,
                    measured_outcome=first.measured_outcome,
                    supporting_excerpt=first.supporting_excerpt,
                    limitations=first.limitations,
                    evidence_strength="weak",
                    is_attributed_only=True,
                    claim_text=first.claim_text,
                )
                idx = findings.index(second)
                findings[idx] = Finding(
                    text=second.text,
                    evidence_ids=second.evidence_ids,
                    status="conflicted",
                    source_type=second.source_type,
                    publication_date=second.publication_date,
                    sample_size=second.sample_size,
                    methodology=second.methodology,
                    measured_outcome=second.measured_outcome,
                    supporting_excerpt=second.supporting_excerpt,
                    limitations=second.limitations,
                    evidence_strength="weak",
                    is_attributed_only=True,
                    claim_text=second.claim_text,
                )

    # Evaluate Independent Verification vs Source Attribution
    # A claim is verified_independent ONLY when corroborated by at least two distinct PRIMARY sources with empirical measurements.
    # Repetition by secondary sources remains attributed only.
    for i, f in enumerate(findings):
        if f.status in ("conflicted", "uncertain"):
            continue
        a = set(re.findall(r"[a-z]{4,}", f.text.lower()))
        corroborating_primaries: list[Evidence] = []
        source_ev = evidence_by_id.get(f.evidence_ids[0])
        if source_ev and source_ev.source_type == "primary":
            corroborating_primaries.append(source_ev)

        for other in findings:
            if other is f or other.status in ("conflicted", "uncertain"):
                continue
            b = set(re.findall(r"[a-z]{4,}", other.text.lower()))
            if len(a & b) >= 4:
                other_ev = evidence_by_id.get(other.evidence_ids[0])
                if (
                    other_ev
                    and other_ev.source_type == "primary"
                    and other_ev.url != (source_ev.url if source_ev else "")
                ):
                    corroborating_primaries.append(other_ev)

        if len(corroborating_primaries) >= 2 and f.measured_outcome:
            # Independent primary empirical replication confirmed
            findings[i] = Finding(
                text=f.text,
                evidence_ids=tuple(sorted({p.evidence_id for p in corroborating_primaries})),
                status="verified_independent",
                source_type="primary",
                publication_date=f.publication_date,
                sample_size=f.sample_size,
                methodology=f.methodology,
                measured_outcome=f.measured_outcome,
                supporting_excerpt=f.supporting_excerpt,
                limitations=f.limitations,
                evidence_strength="strong",
                is_attributed_only=False,
                claim_text=f.claim_text,
            )

    return findings


def validate_references(findings: list[Finding], evidence: list[Evidence]) -> bool:
    known = {item.evidence_id for item in evidence}
    return all(ref in known for finding in findings for ref in finding.evidence_ids)
