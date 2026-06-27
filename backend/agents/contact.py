"""Contact Agent — enriches each company with decision-maker contacts."""

from typing import Any

from graph.state import WorkflowState
from models.agent_kind import AgentKind
from models.business_config import BusinessConfiguration
from agents.base import BaseAgent
from tools.registry import get_contact_enrichment_tool


class ContactAgent(BaseAgent):
    kind = AgentKind.CONTACT

    @property
    def state_key(self) -> str:
        return "contact"

    def _execute(self, state: WorkflowState) -> dict[str, Any]:
        discovery = state.get("discovery", {})
        config = BusinessConfiguration.model_validate(self._get_business_config(state))
        enrich_tool = get_contact_enrichment_tool()

        companies = discovery.get("companies", [])
        if not companies and discovery.get("company_name"):
            companies = [discovery]

        # Enrich each discovered company — real Apollo or labeled mock per company
        enrichment_by_company: list[dict[str, Any]] = []
        integration_records: list[dict[str, Any]] = []

        for company in companies:
            result = enrich_tool.enrich_company(company, config.personas)
            result_data = result.data or {}
            enrichment_by_company.append(result_data)
            integration_records.append({
                "company_name": result_data.get("company_name", ""),
                **result.to_meta(),
            })

        # Flat contact list from primary company for downstream recommendation
        primary = discovery.get("primary_company") or {}
        primary_company_name = (
            primary.get("company_name")
            if isinstance(primary, dict)
            else discovery.get("company_name", "")
        )
        primary_enrichment = next(
            (e for e in enrichment_by_company if e.get("company_name") == primary_company_name),
            enrichment_by_company[0] if enrichment_by_company else {},
        )
        contacts = primary_enrichment.get("contacts", [])

        any_mock = any(r.get("is_mock") for r in integration_records)
        any_real = any(not r.get("is_mock") for r in integration_records if r.get("success"))

        return {
            "enrichment_by_company": enrichment_by_company,
            "contacts": contacts,
            "primary_contact_index": 0,
            "personas_matched": [p.title for p in config.personas],
            "integrations": {
                "per_company": integration_records,
                "summary": {
                    "apollo_configured": any_real,
                    "mock_fallback_used": any_mock,
                },
            },
        }
