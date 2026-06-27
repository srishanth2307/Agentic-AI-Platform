"""Structured schemas for LLM tool outputs."""

from pydantic import BaseModel, Field


class DiscoveredCompany(BaseModel):
    company_name: str
    domain: str = ""
    industry: str = ""
    employee_count: int | None = None
    headquarters: str = ""
    description: str = ""
    signals: list[str] = Field(default_factory=list)
    source_url: str = ""


class CompanyExtractionResult(BaseModel):
    companies: list[DiscoveredCompany] = Field(default_factory=list)
    search_summary: str = ""


class CompanyValidationResult(BaseModel):
    company_name: str
    is_valid: bool
    fit_score: float = Field(ge=0.0, le=1.0)
    checks_passed: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    reasoning: str = ""


class ValidationBatchResult(BaseModel):
    validations: list[CompanyValidationResult] = Field(default_factory=list)
    overall_valid: bool = False
    primary_company: str = ""


class EnrichedContact(BaseModel):
    name: str
    title: str
    email: str = ""
    linkedin_url: str = ""
    phone: str = ""
    department: str = ""
    seniority: str = ""
    pain_points: list[str] = Field(default_factory=list)
    enrichment_source: str = "mock"


class CompanyEnrichmentResult(BaseModel):
    company_name: str
    domain: str
    contacts: list[EnrichedContact] = Field(default_factory=list)
    enrichment_source: str = "mock"
    is_mock: bool = True


class RecommendationOutput(BaseModel):
    summary: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    business_reasoning: str
    recommended_action: str
    priority: str = "medium"
    target_contact: str = ""
    target_title: str = ""
    talking_points: list[str] = Field(default_factory=list)
    draft_subject: str = ""
