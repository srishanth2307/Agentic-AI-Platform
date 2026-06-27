"""LangGraph shared state — passed and mutated across all workflow nodes."""

from typing import Any, TypedDict


class WorkflowState(TypedDict, total=False):
    """
    Single source of truth for a run.

    LangGraph merges partial updates returned by each node into this state.
    Agents read sibling keys (e.g. validation reads `discovery`) instead of
    receiving isolated return values.
    """

    # --- Inputs (set at workflow start) ---
    run_id: str
    goal: str
    business_config: dict[str, Any]

    # --- Planner output ---
    plan: dict[str, Any]

    # --- Agent outputs (each agent writes its own key) ---
    discovery: dict[str, Any]
    validation: dict[str, Any]
    contact: dict[str, Any]
    recommendation: dict[str, Any]

    # --- Run metadata (updated by every node) ---
    status: str
    current_agent: str
    errors: list[str]
