"""Shared interface for all specialized agents."""

import time
from abc import ABC, abstractmethod

from models.agent_context import AgentContext
from models.agent_kind import AgentKind
from models.agent_result import AgentResult


class BaseAgent(ABC):
    """Contract every specialized agent must implement."""

    kind: AgentKind

    def run(self, context: AgentContext) -> AgentResult:
        """Public entry: log start, simulate work, return structured output."""
        print(f"[{self.kind.value.upper()} AGENT] starting (step_id={context.step_id})")
        self._simulate_work()
        data = self._execute(context)
        return AgentResult(agent=self.kind, data=data)

    def _simulate_work(self, seconds: float = 1.0) -> None:
        """Stand-in for LLM calls, tool invocations, and external API latency."""
        time.sleep(seconds)

    @abstractmethod
    def _execute(self, context: AgentContext) -> dict:
        """Agent-specific logic — returns the payload stored in AgentResult.data."""
