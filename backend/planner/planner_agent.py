"""Planner Agent — LangGraph node that builds the execution plan."""

from typing import Any

from graph.state import WorkflowState
from models.business_config import BusinessConfiguration
from models.task import PlannerTask
from planner.planner import Planner


class PlannerAgent:
    """
    First node in the workflow.

    Receives business configuration (ICP, personas, qualification rules) from
    shared state and writes an execution plan back into shared state.
    """

    def run(self, state: WorkflowState) -> dict[str, Any]:
        run_id = state.get("run_id", "unknown")
        print(f"[PLANNER AGENT] starting (run_id={run_id})")

        config = BusinessConfiguration.model_validate(state["business_config"])
        task = PlannerTask(goal=state["goal"], run_id=state.get("run_id"))

        plan = Planner().create_plan(task=task, business_config=config)

        return {
            "plan": plan.model_dump(mode="json"),
            "status": "executing",
            "current_agent": "planner",
        }
