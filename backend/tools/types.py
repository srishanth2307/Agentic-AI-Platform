"""Shared types for reusable tools."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class IntegrationSource(str, Enum):
    """Identifies which integration produced tool output."""

    TAVILY = "tavily"
    FIRECRAWL = "firecrawl"
    GEMINI = "gemini"
    APOLLO = "apollo"
    MOCK = "mock"
    LLM_INFERRED = "llm_inferred"


class ToolResult(BaseModel):
    """
    Standard wrapper for all tool responses.

    Agents must propagate `source` and `is_mock` so the dashboard can
    distinguish real integrations from fallbacks.
    """

    success: bool = True
    source: IntegrationSource
    data: Any = None
    error: str | None = None
    is_mock: bool = False

    def to_meta(self) -> dict[str, Any]:
        """Compact metadata block stored alongside agent payloads."""
        return {
            "integration_source": self.source.value,
            "is_mock": self.is_mock,
            "success": self.success,
            "error": self.error,
        }
