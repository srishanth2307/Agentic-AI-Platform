"""Result of executing a plan through the agent pipeline."""

from typing import Any

from pydantic import BaseModel, Field

from models.agent_result import AgentResult
from models.plan import Plan


class ExecutionResult(BaseModel):
    """Internal result from the agent executor (runner)."""

    run_id: str
    results: list[AgentResult] = Field(default_factory=list)


class RunResult(BaseModel):
    """Combined output from the full orchestration pipeline."""

    run_id: str
    plan_id: str
    status: str = "completed"
    plan: Plan
    results: list[AgentResult]
    memory: dict[str, Any]
