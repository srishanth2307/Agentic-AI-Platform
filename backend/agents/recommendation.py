"""Recommendation Agent — suggests next-best actions (placeholder)."""

from models.agent_context import AgentContext
from models.agent_kind import AgentKind
from agents.base import BaseAgent


class RecommendationAgent(BaseAgent):
    kind = AgentKind.RECOMMENDATION

    def _execute(self, context: AgentContext) -> dict:
        validation = context.prior_results.get(AgentKind.VALIDATION.value, {})
        contact = context.prior_results.get(AgentKind.CONTACT.value, {})
        contacts = contact.get("contacts", [])
        primary = contacts[0] if contacts else {"name": "Unknown", "title": "Unknown"}

        return {
            "recommended_action": "send_intro_email",
            "priority": "high" if validation.get("fit_score", 0) >= 0.8 else "medium",
            "target_contact": primary.get("name"),
            "target_title": primary.get("title"),
            "talking_points": [
                "Reference recent growth signals (placeholder)",
                "Align with their B2B SaaS motion (placeholder)",
                "Offer a short discovery call (placeholder)",
            ],
            "draft_subject": f"Quick idea for {primary.get('name', 'your team')}",
        }
