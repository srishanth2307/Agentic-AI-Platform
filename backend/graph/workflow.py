"""LangGraph workflow definition for ProspectPilot."""

from langgraph.graph import END, START, StateGraph

from graph.nodes import (
    contact_node,
    discovery_node,
    planner_node,
    recommendation_node,
    validation_node,
)
from graph.state import WorkflowState


def build_workflow():
    """
    Build the compiled LangGraph workflow.

    Flow: Planner → Discovery → Validation → Contact → Recommendation → END

    Each node is a thin wrapper around a reusable agent class. The graph
    controls execution order; agents control domain logic and state updates.
    """
    graph = StateGraph(WorkflowState)

    # Register nodes — one LangGraph node per agent
    graph.add_node("planner", planner_node)
    graph.add_node("discovery", discovery_node)
    graph.add_node("validation", validation_node)
    graph.add_node("contact", contact_node)
    graph.add_node("recommendation", recommendation_node)

    # Fixed pipeline edges (Planner decides steps; graph enforces order for Day 2)
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "discovery")
    graph.add_edge("discovery", "validation")
    graph.add_edge("validation", "contact")
    graph.add_edge("contact", "recommendation")
    graph.add_edge("recommendation", END)

    return graph.compile()


# Singleton compiled graph — reused across requests
_compiled_workflow = None


def get_workflow():
    """Return the compiled workflow, creating it on first use."""
    global _compiled_workflow
    if _compiled_workflow is None:
        _compiled_workflow = build_workflow()
    return _compiled_workflow
