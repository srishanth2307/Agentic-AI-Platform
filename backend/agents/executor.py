"""
Legacy sequential executor — superseded by LangGraph (graph/workflow.py).

Kept for reference and tests. New code should use services.WorkflowRunner.
"""

from uuid import uuid4

import memory
from graph.state import WorkflowState
from models.execution import ExecutionResult
from models.plan import Plan
from agents.registry import get_agent


def execute_plan(plan: Plan) -> ExecutionResult:
    """
    Run plan steps without LangGraph (legacy path).

    Prefer WorkflowRunner + get_workflow() for production orchestration.
    """
    run_id = plan.task.run_id or str(uuid4())
    plan.task.run_id = run_id

    memory.save(run_id, "goal", plan.task.goal)
    memory.save(run_id, "plan_id", plan.plan_id)
    memory.save(run_id, "plan", plan.model_dump(mode="json"))

    state: WorkflowState = {
        "run_id": run_id,
        "goal": plan.task.goal,
        "business_config": plan.task.context.get("business_config", {}),
        "status": "executing",
        "errors": [],
    }

    results = []

    for step in sorted(plan.steps, key=lambda s: s.order):
        agent = get_agent(step.agent)
        update = agent.run(state)
        state.update(update)  # type: ignore[typeddict-item]
        memory.save(run_id, step.agent.value, state[step.agent.value])  # type: ignore[literal-required]
        from models.agent_result import AgentResult

        results.append(AgentResult(agent=step.agent, data=state[step.agent.value]))  # type: ignore[literal-required]

    memory.save(run_id, "status", "completed")
    return ExecutionResult(run_id=run_id, results=results)
