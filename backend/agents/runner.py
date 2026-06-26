"""Execute a planner-produced plan through the agent registry (Day 1 harness)."""

from uuid import uuid4

import memory
from models.agent_context import AgentContext
from models.agent_result import AgentResult
from models.plan import Plan
from agents.registry import get_agent


def run_plan(plan: Plan) -> list[AgentResult]:
    """
    Walk plan steps in order, reading/writing shared memory each step.

    Used to validate planner → agent → memory wiring before LangGraph or real AI.
    """
    run_id = plan.task.run_id or str(uuid4())
    memory.save(run_id, "goal", plan.task.goal)
    memory.save(run_id, "plan_id", plan.plan_id)

    results: list[AgentResult] = []

    for step in sorted(plan.steps, key=lambda s: s.order):
        prior_results = memory.load_all(run_id)
        agent = get_agent(step.agent)
        context = AgentContext(
            goal=plan.task.goal,
            step_id=step.step_id,
            run_id=run_id,
            prior_results=prior_results,
        )
        result = agent.run(context)
        memory.save(run_id, step.agent.value, result.model_dump())
        results.append(result)

    return results
