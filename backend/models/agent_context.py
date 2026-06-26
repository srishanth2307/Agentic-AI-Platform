"""Input passed to each specialized agent during a run."""

from typing import Any

from pydantic import BaseModel, Field


class AgentContext(BaseModel):
    """
    Context for a single agent invocation.

    `prior_results` holds outputs from earlier steps in the pipeline so real
    agents (later) can build on discovery data, contacts, etc.
    """

    goal: str
    step_id: str
    run_id: str | None = None
    prior_results: dict[str, Any] = Field(
        default_factory=dict,
        description="Outputs keyed by agent kind value, e.g. 'discovery'",
    )
