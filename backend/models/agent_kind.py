"""Agent identifiers used by the planner and orchestrator."""

from enum import Enum


class AgentKind(str, Enum):
    """Specialized agents the platform can delegate work to."""

    DISCOVERY = "discovery"
    VALIDATION = "validation"
    CONTACT = "contact"
    RECOMMENDATION = "recommendation"
