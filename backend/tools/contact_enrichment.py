"""Contact enrichment — Apollo when configured, mock fallback clearly labeled."""

import httpx

from config.settings import settings
from models.business_config import BusinessConfiguration, Persona
from tools.types import IntegrationSource, ToolResult


class ContactEnrichmentTool:
    """
    Enrich companies with decision-maker contacts.

    Real: Apollo.io people search when APOLLO_API_KEY is set.
    Fallback: mock contacts derived from personas (clearly labeled).
    """

    def enrich_company(
        self,
        company: dict,
        personas: list[Persona],
    ) -> ToolResult:
        if settings.apollo_api_key:
            result = self._enrich_apollo(company, personas)
            if result.success:
                return result
        return self._enrich_mock(company, personas)

    def _enrich_apollo(self, company: dict, personas: list[Persona]) -> ToolResult:
        domain = company.get("domain", "")
        company_name = company.get("company_name", "")
        contacts = []

        try:
            for persona in personas[:3]:
                response = httpx.post(
                    "https://api.apollo.io/v1/mixed_people/search",
                    headers={"X-Api-Key": settings.apollo_api_key or ""},
                    json={
                        "q_organization_domains": domain,
                        "person_titles": [persona.title],
                        "page": 1,
                        "per_page": 1,
                    },
                    timeout=30.0,
                )
                response.raise_for_status()
                people = response.json().get("people", [])
                if people:
                    person = people[0]
                    contacts.append({
                        "name": person.get("name", ""),
                        "title": person.get("title", persona.title),
                        "email": person.get("email", ""),
                        "linkedin_url": person.get("linkedin_url", ""),
                        "phone": person.get("phone_numbers", [{}])[0].get("raw_number", "") if person.get("phone_numbers") else "",
                        "department": persona.department,
                        "seniority": persona.seniority,
                        "pain_points": persona.pain_points,
                        "enrichment_source": "apollo",
                    })

            if contacts:
                return ToolResult(
                    success=True,
                    source=IntegrationSource.APOLLO,
                    data={
                        "company_name": company_name,
                        "domain": domain,
                        "contacts": contacts,
                        "enrichment_source": "apollo",
                        "is_mock": False,
                    },
                    is_mock=False,
                )
            return ToolResult(
                success=False,
                source=IntegrationSource.APOLLO,
                data={},
                error="Apollo returned no contacts for this company",
                is_mock=False,
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                source=IntegrationSource.APOLLO,
                data={},
                error=str(exc),
                is_mock=False,
            )

    @staticmethod
    def _enrich_mock(company: dict, personas: list[Persona]) -> ToolResult:
        domain = company.get("domain", "example.com")
        company_name = company.get("company_name", "Unknown")
        contacts = []

        for persona in personas:
            slug = persona.title.lower().replace(" ", ".")
            contacts.append({
                "name": f"[Mock] {persona.title} Contact",
                "title": persona.title,
                "email": f"{slug}@{domain}",
                "linkedin_url": f"https://linkedin.com/in/mock-{slug}",
                "phone": "",
                "department": persona.department,
                "seniority": persona.seniority,
                "pain_points": persona.pain_points,
                "enrichment_source": "mock",
            })

        if not contacts:
            contacts.append({
                "name": "[Mock] Jane Doe",
                "title": "VP Sales",
                "email": f"jane.doe@{domain}",
                "linkedin_url": "https://linkedin.com/in/mock-jane-doe",
                "phone": "",
                "enrichment_source": "mock",
            })

        return ToolResult(
            success=True,
            source=IntegrationSource.MOCK,
            data={
                "company_name": company_name,
                "domain": domain,
                "contacts": contacts,
                "enrichment_source": "mock",
                "is_mock": True,
            },
            is_mock=True,
            error="APOLLO_API_KEY not configured — using mock contact enrichment",
        )
