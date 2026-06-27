"""Tool registry — reusable capabilities for all agents."""

from tools.company_extraction import CompanyExtractionTool
from tools.contact_enrichment import ContactEnrichmentTool
from tools.llm_client import LLMClient
from tools.qualification import QualificationTool
from tools.recommendation import RecommendationTool
from tools.web_search import WebSearchTool

_web_search: WebSearchTool | None = None
_llm: LLMClient | None = None
_company_extraction: CompanyExtractionTool | None = None
_qualification: QualificationTool | None = None
_contact_enrichment: ContactEnrichmentTool | None = None
_recommendation: RecommendationTool | None = None


def get_web_search_tool() -> WebSearchTool:
    global _web_search
    if _web_search is None:
        _web_search = WebSearchTool()
    return _web_search


def get_llm_client() -> LLMClient:
    global _llm
    if _llm is None:
        _llm = LLMClient()
    return _llm


def get_company_extraction_tool() -> CompanyExtractionTool:
    global _company_extraction
    if _company_extraction is None:
        _company_extraction = CompanyExtractionTool(get_llm_client())
    return _company_extraction


def get_qualification_tool() -> QualificationTool:
    global _qualification
    if _qualification is None:
        _qualification = QualificationTool(get_llm_client())
    return _qualification


def get_contact_enrichment_tool() -> ContactEnrichmentTool:
    global _contact_enrichment
    if _contact_enrichment is None:
        _contact_enrichment = ContactEnrichmentTool()
    return _contact_enrichment


def get_recommendation_tool() -> RecommendationTool:
    global _recommendation
    if _recommendation is None:
        _recommendation = RecommendationTool(get_llm_client())
    return _recommendation
