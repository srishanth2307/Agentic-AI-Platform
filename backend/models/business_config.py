"""Business configuration models for B2B customer discovery."""

from pydantic import BaseModel, Field


class ICP(BaseModel):
    """Ideal Customer Profile — defines who the user wants to reach."""

    industries: list[str] = Field(default_factory=list)
    min_employees: int = Field(default=50, ge=1)
    max_employees: int = Field(default=5000, ge=1)
    regions: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)


class Persona(BaseModel):
    """Target buyer persona within qualified accounts."""

    title: str
    seniority: str = "manager"
    department: str = "Sales"
    pain_points: list[str] = Field(default_factory=list)


class QualificationRules(BaseModel):
    """Rules the Validation Agent applies to discovered prospects."""

    min_fit_score: float = Field(default=0.7, ge=0.0, le=1.0)
    required_signals: list[str] = Field(default_factory=list)
    disqualifiers: list[str] = Field(default_factory=list)


class BusinessConfiguration(BaseModel):
    """
    Full business context the Planner receives before orchestrating agents.

    Drives step descriptions today; will drive LLM planning on a later day.
    """

    icp: ICP
    personas: list[Persona] = Field(default_factory=list)
    qualification_rules: QualificationRules = Field(default_factory=QualificationRules)


def default_business_config() -> BusinessConfiguration:
    """Sensible mock defaults for local development and tests."""
    return BusinessConfiguration(
        icp=ICP(
            industries=["B2B SaaS", "DevTools"],
            min_employees=50,
            max_employees=500,
            regions=["North America", "Europe"],
            keywords=["sales automation", "outbound", "pipeline"],
        ),
        personas=[
            Persona(
                title="VP Sales",
                seniority="executive",
                department="Sales",
                pain_points=["pipeline velocity", "rep productivity"],
            ),
            Persona(
                title="Head of Revenue",
                seniority="executive",
                department="Revenue",
                pain_points=["forecast accuracy", "GTM alignment"],
            ),
        ],
        qualification_rules=QualificationRules(
            min_fit_score=0.7,
            required_signals=["hiring", "funding"],
            disqualifiers=["bankruptcy", "direct competitor"],
        ),
    )
