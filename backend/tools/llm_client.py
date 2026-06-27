"""Reusable LLM client — Gemini when configured, structured mock otherwise."""

import json
import re
from collections.abc import Callable
from typing import TypeVar

from pydantic import BaseModel

from config.settings import settings
from tools.types import IntegrationSource, ToolResult

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    """
    Wraps LangChain ChatGoogleGenerativeAI for structured JSON extraction.

    Falls back to deterministic mock output when GEMINI_API_KEY is missing,
    always labeling the source clearly.
    """

    def __init__(self) -> None:
        self._llm = None
        if settings.gemini_api_key:
            from langchain_google_genai import ChatGoogleGenerativeAI

            self._llm = ChatGoogleGenerativeAI(
                model=settings.gemini_model,
                google_api_key=settings.gemini_api_key,
                temperature=0.2,
            )

    @property
    def is_available(self) -> bool:
        return self._llm is not None

    def invoke_structured(
        self,
        prompt: str,
        schema: type[T],
        *,
        mock_factory: Callable[[], T],
    ) -> ToolResult:
        """Run LLM with JSON schema instruction, or return labeled mock."""
        if not self.is_available:
            mock_data = mock_factory()
            return ToolResult(
                success=True,
                source=IntegrationSource.MOCK,
                data=mock_data.model_dump() if isinstance(mock_data, BaseModel) else mock_data,
                is_mock=True,
                error="GEMINI_API_KEY not configured — using mock LLM output",
            )

        schema_json = json.dumps(schema.model_json_schema(), indent=2)
        full_prompt = (
            f"{prompt}\n\n"
            "Respond with valid JSON only matching this schema:\n"
            f"{schema_json}"
        )

        try:
            response = self._llm.invoke(full_prompt)
            content = response.content
            if isinstance(content, list):
                content = "".join(
                    block.get("text", "") if isinstance(block, dict) else str(block)
                    for block in content
                )
            text = str(content).strip()
            # Strip markdown fences if the model wraps JSON
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\s*", "", text)
                text = re.sub(r"\s*```$", "", text)
            parsed = schema.model_validate(json.loads(text))
            return ToolResult(
                success=True,
                source=IntegrationSource.GEMINI,
                data=parsed.model_dump(),
                is_mock=False,
            )
        except Exception as exc:
            mock_data = mock_factory()
            return ToolResult(
                success=False,
                source=IntegrationSource.MOCK,
                data=mock_data.model_dump() if isinstance(mock_data, BaseModel) else mock_data,
                is_mock=True,
                error=f"LLM call failed ({exc}) — using mock fallback",
            )
