"""Shared interface for all LangGraph-backed agents."""

from abc import ABC, abstractmethod
from typing import Any

from graph.state import WorkflowState
from models.agent_kind import AgentKind


class BaseAgent(ABC):
    """
    Reusable agent base class.

    Each agent reads from WorkflowState and returns a *partial state update*
    that LangGraph merges into shared state. Agents call reusable tools from
    the tools/ layer — never embed API logic directly.
    """

    kind: AgentKind

    @property
    @abstractmethod
    def state_key(self) -> str:
        """Key this agent writes in WorkflowState (e.g. 'discovery')."""

    def run(self, state: WorkflowState) -> dict[str, Any]:
        """Public entry: log, execute via tools, return state patch."""
        run_id = state.get("run_id", "unknown")
        print(f"[{self.kind.value.upper()} AGENT] starting (run_id={run_id})")
        payload = self._execute(state)
        return {
            self.state_key: payload,
            "current_agent": self.kind.value,
        }

    @abstractmethod
    def _execute(self, state: WorkflowState) -> dict[str, Any]:
        """
        Agent-specific logic using reusable tools.

        Read from `state`, call tools from tools.registry, return payload
        for `state_key`. Include `integrations` metadata in the payload.
        """

    @staticmethod
    def _get_business_config(state: WorkflowState) -> dict[str, Any]:
        """Helper: extract business configuration from shared state."""
        return state.get("business_config", {})
