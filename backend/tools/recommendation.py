"""LLM-powered explainable recommendation generation."""

import json

from tools.llm_client import LLMClient
from tools.schemas import RecommendationOutput
from tools.types import ToolResult


class RecommendationTool:
    """Generate explainable outreach recommendation with confidence score."""

    def __init__(self, llm: LLMClient | None = None) -> None:
        self._llm = llm or LLMClient()

    def generate(self, workflow_snapshot: dict) -> ToolResult:
        prompt = (
            "You are a B2B sales strategist. Based on the full prospect discovery workflow below, "
            "produce an explainable recommendation.\n\n"
            f"Workflow data:\n{json.dumps(workflow_snapshot, indent=2, default=str)}\n\n"
            "Include:\n"
            "- summary: 2-3 sentence executive summary\n"
            "- confidence_score: 0-1 how confident you are in this recommendation\n"
            "- business_reasoning: why this prospect and action make sense\n"
            "- recommended_action: e.g. send_intro_email, nurture, disqualify\n"
            "- priority: high, medium, or low\n"
            "- target_contact and target_title from enriched contacts\n"
            "- talking_points: 3 specific points\n"
            "- draft_subject: email subject line"
        )

        validation = workflow_snapshot.get("validation", {})
        contact = workflow_snapshot.get("contact", {})
        discovery = workflow_snapshot.get("discovery", {})
        contacts = contact.get("contacts", [])
        primary = contacts[0] if contacts else {}

        def mock_factory() -> RecommendationOutput:
            validations = validation.get("validations", [])
            primary_val = validations[0] if validations else validation
            fit = primary_val.get("fit_score", validation.get("fit_score", 0.82))
            is_valid = primary_val.get("is_valid", validation.get("is_valid", validation.get("overall_valid", True)))
            primary_co = discovery.get("primary_company") or {}
            co_name = primary_co.get("company_name", discovery.get("company_name", "identified")) if isinstance(primary_co, dict) else discovery.get("company_name", "identified")
            return RecommendationOutput(
                summary=(
                    f"{'Qualified' if is_valid else 'Borderline'} prospect {co_name} "
                    "matches ICP criteria. Recommend personalized outreach to the primary contact."
                ),
                confidence_score=min(float(fit), 0.95),
                business_reasoning=(
                    "Mock reasoning — configure GEMINI_API_KEY for LLM-generated business analysis. "
                    "Company shows ICP industry alignment and actionable contact data."
                ),
                recommended_action="send_intro_email" if is_valid else "nurture",
                priority="high" if float(fit) >= 0.8 else "medium",
                target_contact=primary.get("name", "Unknown"),
                target_title=primary.get("title", "Unknown"),
                talking_points=[
                    "Reference ICP-aligned growth signals",
                    "Connect product value to persona pain points",
                    "Propose a low-friction discovery call",
                ],
                draft_subject=f"Idea for {primary.get('name', 'your team')}",
            )

        return self._llm.invoke_structured(prompt, RecommendationOutput, mock_factory=mock_factory)
