"""Maps AgentKind → reusable agent instances for the registry pattern."""

from models.agent_kind import AgentKind
from agents.base import BaseAgent
from agents.contact import ContactAgent
from agents.discovery import DiscoveryAgent
from agents.recommendation import RecommendationAgent
from agents.validation import ValidationAgent

_AGENT_REGISTRY: dict[AgentKind, BaseAgent] = {
    AgentKind.DISCOVERY: DiscoveryAgent(),
    AgentKind.VALIDATION: ValidationAgent(),
    AgentKind.CONTACT: ContactAgent(),
    AgentKind.RECOMMENDATION: RecommendationAgent(),
}


def get_agent(kind: AgentKind) -> BaseAgent:
    """Return the agent implementation for a given kind."""
    try:
        return _AGENT_REGISTRY[kind]
    except KeyError as exc:
        raise ValueError(f"No agent registered for kind: {kind}") from exc
