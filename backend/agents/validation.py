"""Validation Agent — verifies data quality and ICP fit (placeholder)."""

from models.agent_context import AgentContext
from models.agent_kind import AgentKind
from agents.base import BaseAgent


class ValidationAgent(BaseAgent):
    kind = AgentKind.VALIDATION

    def _execute(self, context: AgentContext) -> dict:
        discovery = context.prior_results.get(AgentKind.DISCOVERY.value, {})
        company = discovery.get("company_name", "Unknown")

        return {
            "is_valid": True,
            "fit_score": 0.82,
            "validated_company": company,
            "checks_passed": [
                "domain_resolves",
                "icp_industry_match",
                "minimum_headcount",
            ],
            "warnings": [],
        }
