"""LLM-powered company extraction from web search results."""

import json

from models.business_config import BusinessConfiguration
from tools.llm_client import LLMClient
from tools.schemas import CompanyExtractionResult, DiscoveredCompany
from tools.types import ToolResult


class CompanyExtractionTool:
    """Parse web search hits into structured companies matching an ICP."""

    def __init__(self, llm: LLMClient | None = None) -> None:
        self._llm = llm or LLMClient()

    def extract(
        self,
        search_result: ToolResult,
        config: BusinessConfiguration,
        goal: str,
    ) -> ToolResult:
        search_data = search_result.data or {}
        hits = search_data.get("results", [])
        icp = config.icp

        prompt = (
            f"Goal: {goal}\n\n"
            f"ICP industries: {', '.join(icp.industries)}\n"
            f"Employee range: {icp.min_employees}-{icp.max_employees}\n"
            f"Regions: {', '.join(icp.regions)}\n"
            f"Keywords: {', '.join(icp.keywords)}\n\n"
            f"Search answer: {search_data.get('answer', '')}\n\n"
            f"Search results:\n{json.dumps(hits, indent=2)}\n\n"
            "Extract up to 5 companies that best match the ICP. "
            "Include signals like funding, hiring, or growth where visible."
        )

        def mock_factory() -> CompanyExtractionResult:
            industry = icp.industries[0] if icp.industries else "B2B SaaS"
            return CompanyExtractionResult(
                search_summary="Mock extraction — configure GEMINI_API_KEY for LLM parsing.",
                companies=[
                    DiscoveredCompany(
                        company_name="Acme Corp",
                        domain="acme.example",
                        industry=industry,
                        employee_count=max(icp.min_employees, 250),
                        headquarters=icp.regions[0] if icp.regions else "North America",
                        description="B2B SaaS sales platform (mock)",
                        signals=["Series B funding (mock)", "Hiring VP Sales (mock)"],
                        source_url="https://acme.example/about",
                    ),
                    DiscoveredCompany(
                        company_name="NovaStack",
                        domain="novastack.io",
                        industry=icp.industries[1] if len(icp.industries) > 1 else industry,
                        employee_count=120,
                        headquarters=icp.regions[0] if icp.regions else "North America",
                        description="Developer tools company (mock)",
                        signals=["Outbound GTM motion (mock)"],
                        source_url="https://novastack.io",
                    ),
                ],
            )

        llm_result = self._llm.invoke_structured(prompt, CompanyExtractionResult, mock_factory=mock_factory)
        # Propagate search mock status if LLM succeeded but search was mock
        if search_result.is_mock and not llm_result.is_mock:
            llm_result.is_mock = True
            llm_result.error = (llm_result.error or "") + " | Search results were mock"
        return llm_result
