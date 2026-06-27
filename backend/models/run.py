"""HTTP request/response schemas for agent runs."""

from typing import Any

from pydantic import BaseModel, Field

from models.agent_result import AgentResult
from models.business_config import BusinessConfiguration
from models.plan import Plan


class RunRequest(BaseModel):
    """Body for POST /runs — starts LangGraph planner → agent pipeline."""

    goal: str = Field(..., min_length=1, description="Natural-language task from the user")
    run_id: str | None = Field(
        default=None,
        description="Optional run id; generated if omitted",
    )
    business_config: BusinessConfiguration | None = Field(
        default=None,
        description="ICP, personas, and qualification rules; uses defaults if omitted",
    )


class RunResponse(BaseModel):
    """Full run result returned after LangGraph workflow completes."""

    run_id: str
    plan_id: str
    status: str = "completed"
    plan: Plan
    results: list[AgentResult]
    memory: dict[str, Any]
