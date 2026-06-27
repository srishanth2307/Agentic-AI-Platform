"""Recommendation Agent — LLM explainable summary with confidence and next action."""

from typing import Any

from graph.state import WorkflowState
from models.agent_kind import AgentKind
from agents.base import BaseAgent
from tools.registry import get_recommendation_tool


class RecommendationAgent(BaseAgent):
    kind = AgentKind.RECOMMENDATION

    @property
    def state_key(self) -> str:
        return "recommendation"

    def _execute(self, state: WorkflowState) -> dict[str, Any]:
        # Snapshot shared state for the LLM recommendation tool
        snapshot = {
            "goal": state.get("goal", ""),
            "business_config": state.get("business_config", {}),
            "discovery": state.get("discovery", {}),
            "validation": state.get("validation", {}),
            "contact": state.get("contact", {}),
        }

        rec_tool = get_recommendation_tool()
        rec_result = rec_tool.generate(snapshot)
        rec_data = rec_result.data or {}

        return {
            **rec_data,
            "integrations": {
                "recommendation": rec_result.to_meta(),
            },
        }
