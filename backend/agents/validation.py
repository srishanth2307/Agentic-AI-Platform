"""Validation Agent — LLM qualification against ICP and business rules."""

from typing import Any

from graph.state import WorkflowState
from models.agent_kind import AgentKind
from models.business_config import BusinessConfiguration
from agents.base import BaseAgent
from tools.registry import get_qualification_tool


class ValidationAgent(BaseAgent):
    kind = AgentKind.VALIDATION

    @property
    def state_key(self) -> str:
        return "validation"

    def _execute(self, state: WorkflowState) -> dict[str, Any]:
        discovery = state.get("discovery", {})
        config = BusinessConfiguration.model_validate(self._get_business_config(state))

        # Support multi-company discovery output or legacy single-company shape
        companies = discovery.get("companies", [])
        if not companies and discovery.get("company_name"):
            companies = [discovery]

        # Tool: LLM evaluates each company against qualification rules
        qual_tool = get_qualification_tool()
        qual_result = qual_tool.evaluate(companies, config)
        qual_data = qual_result.data or {}
        validations = qual_data.get("validations", [])

        primary_name = qual_data.get("primary_company", "")
        primary_validation = next(
            (v for v in validations if v.get("company_name") == primary_name),
            validations[0] if validations else {},
        )

        return {
            "validations": validations,
            "overall_valid": qual_data.get("overall_valid", False),
            "primary_company": primary_name,
            # Backward-compatible fields used by Recommendation agent
            "is_valid": primary_validation.get("is_valid", False),
            "fit_score": primary_validation.get("fit_score", 0.0),
            "validated_company": primary_validation.get("company_name", primary_name),
            "checks_passed": primary_validation.get("checks_passed", []),
            "warnings": primary_validation.get("warnings", []),
            "reasoning": primary_validation.get("reasoning", ""),
            "qualification_rules_applied": config.qualification_rules.model_dump(),
            "integrations": {
                "qualification": qual_result.to_meta(),
            },
        }
