"""Day 1 fixed pipeline — no LLM, no branching."""

from models.agent_kind import AgentKind

# Canonical execution order for every task on Day 1.
FIXED_AGENT_SEQUENCE: tuple[AgentKind, ...] = (
    AgentKind.DISCOVERY,
    AgentKind.VALIDATION,
    AgentKind.CONTACT,
    AgentKind.RECOMMENDATION,
)

# Default intent text per agent; {goal} is filled from the task at plan time.
STEP_TEMPLATES: dict[AgentKind, str] = {
    AgentKind.DISCOVERY: (
        "Run Discovery Agent: gather prospect and company signals for «{goal}»."
    ),
    AgentKind.VALIDATION: (
        "Run Validation Agent: verify data quality and fit for «{goal}»."
    ),
    AgentKind.CONTACT: (
        "Run Contact Agent: identify and enrich decision-maker contacts for «{goal}»."
    ),
    AgentKind.RECOMMENDATION: (
        "Run Recommendation Agent: produce next-best actions for «{goal}»."
    ),
}
