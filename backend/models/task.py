"""Input model: what the planner receives from the API or orchestrator."""

from typing import Any

from pydantic import BaseModel, Field


class PlannerTask(BaseModel):
    """
    A unit of work for the planner.

    Day 1: only `goal` affects routing (fixed pipeline regardless of content).
    Later: `goal` + `context` will inform LLM-generated step selection.
    """

    goal: str = Field(..., min_length=1, description="Natural-language objective from the user")
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional metadata (company name, user id, constraints)",
    )
    run_id: str | None = Field(
        default=None,
        description="Platform run identifier; links the plan to shared memory",
    )
