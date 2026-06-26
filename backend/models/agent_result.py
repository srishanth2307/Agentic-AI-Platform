"""Output returned by each specialized agent."""

from typing import Any

from pydantic import BaseModel, Field

from models.agent_kind import AgentKind


class AgentResult(BaseModel):
    """Structured result stored in shared memory and shown on the dashboard."""

    agent: AgentKind
    status: str = Field(default="completed")
    data: dict[str, Any]
