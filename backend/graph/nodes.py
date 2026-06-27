"""LangGraph node functions — thin adapters between graph and agent classes."""

from graph.persistence import persist_state_update
from graph.state import WorkflowState
from planner.planner_agent import PlannerAgent
from agents.contact import ContactAgent
from agents.discovery import DiscoveryAgent
from agents.recommendation import RecommendationAgent
from agents.validation import ValidationAgent

# Reusable agent instances — stateless, safe to share across invocations
_planner = PlannerAgent()
_discovery = DiscoveryAgent()
_validation = ValidationAgent()
_contact = ContactAgent()
_recommendation = RecommendationAgent()


def _run_node(state: WorkflowState, agent) -> dict:
    """
    Execute an agent against shared state and persist the update.

    Every node follows the same pattern: run → persist → return partial state.
    """
    update = agent.run(state)
    run_id = state.get("run_id", "")
    if run_id:
        persist_state_update(run_id, update)
    return update


def planner_node(state: WorkflowState) -> dict:
    """LangGraph node: Planner Agent — builds execution plan from business config."""
    return _run_node(state, _planner)


def discovery_node(state: WorkflowState) -> dict:
    """LangGraph node: Discovery Agent — gathers prospect signals."""
    return _run_node(state, _discovery)


def validation_node(state: WorkflowState) -> dict:
    """LangGraph node: Validation Agent — checks ICP fit and qualification rules."""
    return _run_node(state, _validation)


def contact_node(state: WorkflowState) -> dict:
    """LangGraph node: Contact Agent — maps personas to decision-makers."""
    return _run_node(state, _contact)


def recommendation_node(state: WorkflowState) -> dict:
    """LangGraph node: Recommendation Agent — produces next-best actions."""
    update = _run_node(state, _recommendation)
    # Mark run complete after the final agent
    completion = {"status": "completed", "current_agent": "done"}
    run_id = state.get("run_id", "")
    if run_id:
        persist_state_update(run_id, completion)
    return {**update, **completion}
