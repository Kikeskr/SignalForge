"""Markdown and JSON report output."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from signalforge.evidence import Evidence
from signalforge.verify import Finding


def write_report(question: str, evidence: list[Evidence], findings: list[Finding], output: Path,
                 metadata: dict[str, Any] | None = None) -> tuple[Path, Path]:
    output.mkdir(parents=True, exist_ok=True)
    report_path = output / "report.md"
    ledger_path = output / "evidence.json"
    meta_path = output / "run.json"
    lines = ["# SignalForge research report", "", f"**Question:** {question}", "",
             "## Findings", ""]
    for finding in findings:
        refs = ", ".join(f"[{ref}]" for ref in finding.evidence_ids)
        lines.append(f"- **{finding.status}** {finding.text} {refs}")
    if not findings:
        lines.append("No usable source excerpts were found; no findings are asserted.")
    lines.extend(["", "## Sources", ""])
    for item in evidence:
        lines.append(f"- [{item.evidence_id}] [{item.title}]({item.url}) — retrieved {item.retrieved_at}")
    lines.extend(["", "## Limitations", "",
                  "Findings reproduce retrieved source excerpts and link each to its source. `partially_supported` means source-attributed evidence was captured; it is not independent verification of the factual claim. Contradiction labels use a small lexical heuristic and require human review. This run does not use a language model.", ""])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    payload = {"question": question, "sources": [asdict(item) for item in evidence],
               "findings": [asdict(item) for item in findings]}
    ledger_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if metadata is not None:
        meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return report_path, ledger_path
