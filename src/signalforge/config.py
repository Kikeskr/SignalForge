"""Small, secret-safe configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    model_api_key: str | None
    search_api_key: str | None
    neatlogs_api_key: str | None


def load_settings() -> Settings:
    """Read only supported credential names; never log their contents."""
    return Settings(
        model_api_key=os.getenv("LITELLM_API_KEY"),
        search_api_key=os.getenv("TAVILY_API_KEY"),
        neatlogs_api_key=os.getenv("NEATLOGS_API_KEY"),
    )
