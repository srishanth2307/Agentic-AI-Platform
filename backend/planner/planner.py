"""Planner Agent — Day 1: fixed agent sequence (no LLM)."""

from uuid import uuid4

from models.agent_kind import AgentKind
from models.plan import Plan, PlanStep
from models.task import PlannerTask
from planner.sequence import FIXED_AGENT_SEQUENCE, STEP_TEMPLATES


class Planner:
    """
    Converts a user task into an ordered execution plan.

    Day 1 behavior: always emit the same four agents in the same order.
    The public method `create_plan` stays stable so callers (API, LangGraph)
    do not change when we swap in LLM-based planning later.
    """

    def create_plan(self, task: PlannerTask) -> Plan:
        """
        Entry point: task in, plan out.

        This is the only method external code should call today.
        """
        steps = self._build_fixed_steps(task)
        return Plan(
            plan_id=str(uuid4()),
            task=task,
            steps=steps,
        )

    def _build_fixed_steps(self, task: PlannerTask) -> list[PlanStep]:
        """
        Day 1 strategy: walk a hard-coded agent sequence.

        No LLM, no conditionals — every task gets Discovery → Validation
        → Contact → Recommendation.
        """
        return [
            self._make_step(order=index, agent=agent, task=task)
            for index, agent in enumerate(FIXED_AGENT_SEQUENCE, start=1)
        ]

    def _make_step(self, order: int, agent: AgentKind, task: PlannerTask) -> PlanStep:
        """Build a single PlanStep with a stable id and templated description."""
        return PlanStep(
            step_id=str(uuid4()),
            order=order,
            agent=agent,
            description=self._describe_step(agent=agent, goal=task.goal),
        )

    @staticmethod
    def _describe_step(agent: AgentKind, goal: str) -> str:
        """Fill the step template with the user's goal for dashboard readability."""
        template = STEP_TEMPLATES[agent]
        return template.format(goal=goal)
