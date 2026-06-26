"""Discovery Agent — gathers prospect and company signals (placeholder)."""

from models.agent_context import AgentContext
from models.agent_kind import AgentKind
from agents.base import BaseAgent


class DiscoveryAgent(BaseAgent):
    kind = AgentKind.DISCOVERY

    def _execute(self, context: AgentContext) -> dict:
        return {
            "company_name": "Acme Corp",
            "domain": "acme.example",
            "industry": "B2B SaaS",
            "employee_count": 250,
            "headquarters": "San Francisco, CA",
            "signals": [
                "Series B funding (placeholder)",
                "Hiring VP Sales (placeholder)",
            ],
            "source_goal": context.goal,
        }
