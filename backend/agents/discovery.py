"""Discovery Agent — web search + LLM extraction of ICP-matching companies."""

from typing import Any

from graph.state import WorkflowState
from models.agent_kind import AgentKind
from models.business_config import BusinessConfiguration
from agents.base import BaseAgent
from tools.registry import get_company_extraction_tool, get_web_search_tool


class DiscoveryAgent(BaseAgent):
    kind = AgentKind.DISCOVERY

    @property
    def state_key(self) -> str:
        return "discovery"

    def _execute(self, state: WorkflowState) -> dict[str, Any]:
        config = BusinessConfiguration.model_validate(self._get_business_config(state))
        goal = state.get("goal", "")
        icp = config.icp

        # Build a targeted search query from ICP + user goal
        industry_clause = ", ".join(icp.industries[:3]) if icp.industries else "B2B companies"
        region_clause = ", ".join(icp.regions[:2]) if icp.regions else ""
        keyword_clause = ", ".join(icp.keywords[:3]) if icp.keywords else ""
        search_query = (
            f"{goal}. {industry_clause} companies"
            f"{f' in {region_clause}' if region_clause else ''}"
            f"{f' related to {keyword_clause}' if keyword_clause else ''}"
            f" with {icp.min_employees}-{icp.max_employees} employees"
        )

        # Tool 1: web search (Tavily → Firecrawl → mock)
        search_tool = get_web_search_tool()
        search_result = search_tool.search(search_query, max_results=5)

        # Tool 2: LLM extracts structured companies from search hits
        extraction_tool = get_company_extraction_tool()
        extraction_result = extraction_tool.extract(search_result, config, goal)
        extraction_data = extraction_result.data or {}
        companies = extraction_data.get("companies", [])
        primary = companies[0] if companies else {}

        return {
            "companies": companies,
            "primary_company": primary,
            # Backward-compatible top-level fields for downstream agents
            "company_name": primary.get("company_name", ""),
            "domain": primary.get("domain", ""),
            "industry": primary.get("industry", ""),
            "employee_count": primary.get("employee_count"),
            "headquarters": primary.get("headquarters", ""),
            "signals": primary.get("signals", []),
            "search_query": search_query,
            "search_summary": extraction_data.get("search_summary", ""),
            "source_goal": goal,
            "icp_industries_targeted": icp.industries,
            "integrations": {
                "search": search_result.to_meta(),
                "extraction": extraction_result.to_meta(),
            },
        }
