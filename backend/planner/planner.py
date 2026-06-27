"""Planner Agent — builds execution plan from task + business configuration."""

from uuid import uuid4

from models.agent_kind import AgentKind
from models.business_config import BusinessConfiguration
from models.plan import Plan, PlanStep
from models.task import PlannerTask
from planner.sequence import FIXED_AGENT_SEQUENCE, STEP_TEMPLATES


class Planner:
    """
    Converts a user task + business configuration into an ordered plan.

    Day 2: fixed agent sequence, but step descriptions are tailored to ICP
    and personas. Later this class will call an LLM for dynamic planning.
    """

    def create_plan(
        self,
        task: PlannerTask,
        business_config: BusinessConfiguration | None = None,
    ) -> Plan:
        """Entry point: task + config in, plan out."""
        steps = self._build_fixed_steps(task, business_config)
        return Plan(
            plan_id=str(uuid4()),
            task=task,
            steps=steps,
        )

    def _build_fixed_steps(
        self,
        task: PlannerTask,
        business_config: BusinessConfiguration | None,
    ) -> list[PlanStep]:
        """
        Day 2 strategy: fixed pipeline order, config-aware descriptions.

        Order is always Discovery → Validation → Contact → Recommendation.
        """
        return [
            self._make_step(
                order=index,
                agent=agent,
                task=task,
                business_config=business_config,
            )
            for index, agent in enumerate(FIXED_AGENT_SEQUENCE, start=1)
        ]

    def _make_step(
        self,
        order: int,
        agent: AgentKind,
        task: PlannerTask,
        business_config: BusinessConfiguration | None,
    ) -> PlanStep:
        return PlanStep(
            step_id=str(uuid4()),
            order=order,
            agent=agent,
            description=self._describe_step(agent, task.goal, business_config),
        )

    @staticmethod
    def _describe_step(
        agent: AgentKind,
        goal: str,
        business_config: BusinessConfiguration | None,
    ) -> str:
        """Fill step template; append ICP context when config is available."""
        base = STEP_TEMPLATES[agent].format(goal=goal)
        if business_config is None:
            return base

        icp = business_config.icp
        icp_hint = (
            f" [ICP: {', '.join(icp.industries[:2])}, "
            f"{icp.min_employees}-{icp.max_employees} employees]"
        )
        return base + icp_hint
