"""Contact Agent — identifies decision-makers (placeholder)."""

from models.agent_context import AgentContext
from models.agent_kind import AgentKind
from agents.base import BaseAgent


class ContactAgent(BaseAgent):
    kind = AgentKind.CONTACT

    def _execute(self, context: AgentContext) -> dict:
        discovery = context.prior_results.get(AgentKind.DISCOVERY.value, {})
        domain = discovery.get("domain", "example.com")

        return {
            "contacts": [
                {
                    "name": "Jane Doe",
                    "title": "VP Sales",
                    "email": f"jane.doe@{domain}",
                    "linkedin_url": "https://linkedin.com/in/jane-doe-placeholder",
                },
                {
                    "name": "John Smith",
                    "title": "Head of Revenue",
                    "email": f"john.smith@{domain}",
                    "linkedin_url": "https://linkedin.com/in/john-smith-placeholder",
                },
            ],
            "primary_contact_index": 0,
        }
