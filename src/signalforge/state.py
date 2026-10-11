"""Atomic JSON persistence for research runs."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any

from signalforge.evidence import Evidence


def save_evidence(path: Path, evidence: list[Evidence]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(item) for item in evidence]
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
        temporary = Path(stream.name)
    os.replace(temporary, path)


def load_evidence(path: Path) -> list[Evidence]:
    rows: list[dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))
    return [Evidence(**row) for row in rows]
