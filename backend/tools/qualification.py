"""LLM-powered qualification against ICP and business rules."""

import json

from models.business_config import BusinessConfiguration
from tools.llm_client import LLMClient
from tools.schemas import CompanyValidationResult, ValidationBatchResult
from tools.types import ToolResult


class QualificationTool:
    """Evaluate discovered companies against qualification criteria using an LLM."""

    def __init__(self, llm: LLMClient | None = None) -> None:
        self._llm = llm or LLMClient()

    def evaluate(
        self,
        companies: list[dict],
        config: BusinessConfiguration,
    ) -> ToolResult:
        rules = config.qualification_rules
        icp = config.icp

        prompt = (
            "Evaluate each company against the ICP and qualification rules.\n\n"
            f"ICP: {json.dumps(icp.model_dump(), indent=2)}\n\n"
            f"Qualification rules: {json.dumps(rules.model_dump(), indent=2)}\n\n"
            f"Companies to evaluate:\n{json.dumps(companies, indent=2)}\n\n"
            "For each company return is_valid, fit_score (0-1), checks_passed, "
            "warnings, and reasoning explaining the decision. "
            "Set overall_valid true if the best company meets min_fit_score. "
            "Set primary_company to the highest-scoring valid company name."
        )

        def mock_factory() -> ValidationBatchResult:
            validations = []
            for idx, company in enumerate(companies):
                name = company.get("company_name", f"Company {idx + 1}")
                industry = company.get("industry", "")
                employees = company.get("employee_count") or 0
                industry_match = industry in icp.industries if icp.industries else True
                size_match = icp.min_employees <= employees <= icp.max_employees if employees else True
                fit = 0.82 if industry_match and size_match else 0.55
                validations.append(
                    CompanyValidationResult(
                        company_name=name,
                        is_valid=fit >= rules.min_fit_score,
                        fit_score=fit,
                        checks_passed=[
                            c for c, ok in [
                                ("icp_industry_match", industry_match),
                                ("icp_size_match", size_match),
                            ] if ok
                        ],
                        warnings=[] if fit >= rules.min_fit_score else ["Below minimum fit score"],
                        reasoning="Mock validation — configure GEMINI_API_KEY for LLM evaluation.",
                    )
                )
            best = max(validations, key=lambda v: v.fit_score) if validations else None
            return ValidationBatchResult(
                validations=validations,
                overall_valid=best.is_valid if best else False,
                primary_company=best.company_name if best else "",
            )

        return self._llm.invoke_structured(prompt, ValidationBatchResult, mock_factory=mock_factory)
