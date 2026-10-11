"""Optional, content-minimizing neatlogs spans for real workflow operations."""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager
from importlib import import_module
from typing import Any, cast


@contextmanager
def workflow_span() -> Iterator[None]:
    key = os.getenv("NEATLOGS_API_KEY")
    if not key:
        yield
        return
    neatlogs = cast(Any, import_module("neatlogs"))

    neatlogs.init(api_key=key, workflow_name="signalforge-research")
    try:
        with neatlogs.trace("research_run", kind="WORKFLOW"):
            yield
    finally:
        neatlogs.flush()
        neatlogs.shutdown()


@contextmanager
def operation_span(name: str) -> Iterator[Any | None]:
    if not os.getenv("NEATLOGS_API_KEY"):
        yield None
        return
    neatlogs = cast(Any, import_module("neatlogs"))

    with neatlogs.trace(name, kind="TOOL") as span:
        span.set_attribute("neatlogs.tool.name", name)
        try:
            yield span
        except Exception as exc:
            span.set_attribute("signalforge.outcome", "error")
            span.set_attribute("signalforge.error_type", type(exc).__name__)
            raise
        else:
            span.set_attribute("signalforge.outcome", "success")
