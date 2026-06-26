"""Output models: the structured plan the planner produces."""

from datetime import datetime, timezone

from pydantic import BaseModel, Field

from models.agent_kind import AgentKind
from models.task import PlannerTask


class PlanStep(BaseModel):
    """One step in an execution plan — maps to a single specialized agent invocation."""

    step_id: str
    order: int = Field(..., ge=1, description="1-based position in the pipeline")
    agent: AgentKind
    description: str = Field(..., description="Human-readable intent for this step")


class Plan(BaseModel):
    """Ordered list of agent steps derived from a task."""

    plan_id: str
    task: PlannerTask
    steps: list[PlanStep]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
