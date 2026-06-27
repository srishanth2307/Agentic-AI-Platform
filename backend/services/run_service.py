"""Orchestrates LangGraph workflow → memory → API response."""

from datetime import datetime, timezone

import memory
from models.agent_kind import AgentKind
from models.agent_result import AgentResult
from models.business_config import BusinessConfiguration, default_business_config
from models.execution import RunResult
from models.plan import Plan
from models.run import RunRequest, RunResponse
from services.workflow_runner import WorkflowRunner


class RunService:
    """
    Production entry point for agent runs.

    Uses LangGraph for orchestration. The sequential executor (agents/executor.py)
    is kept for reference but is no longer the primary path.
    """

    def __init__(self, workflow_runner: WorkflowRunner | None = None) -> None:
        self._runner = workflow_runner or WorkflowRunner()

    def execute(self, request: RunRequest) -> RunResponse:
        """Full pipeline via LangGraph: plan → agents → memory → JSON."""
        config = request.business_config or default_business_config()
        final_state = self._runner.run(
            goal=request.goal,
            business_config=config,
            run_id=request.run_id,
        )
        result = self._build_run_result(final_state)

        return RunResponse(
            run_id=result.run_id,
            plan_id=result.plan_id,
            status=result.status,
            plan=result.plan,
            results=result.results,
            memory=result.memory,
        )

    def stream(self, request: RunRequest):
        """Yield SSE-friendly events for live dashboard updates."""
        config = request.business_config or default_business_config()
        run_id = request.run_id

        try:
            for event in self._runner.stream(
                goal=request.goal,
                business_config=config,
                run_id=run_id,
            ):
                if event.get("event") == "run_completed":
                    result = self._build_run_result(event["state"])
                    event["response"] = RunResponse(
                        run_id=result.run_id,
                        plan_id=result.plan_id,
                        status=result.status,
                        plan=result.plan,
                        results=result.results,
                        memory=result.memory,
                    ).model_dump(mode="json")
                    event.pop("state", None)
                yield event
        except Exception as exc:
            yield {
                "event": "run_failed",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "run_id": run_id or "",
                "agent": "system",
                "status": "failed",
                "progress": 0,
                "error": str(exc),
            }

    def _build_run_result(self, state: dict) -> RunResult:
        run_id = state["run_id"]
        plan_data = state.get("plan")
        if not plan_data:
            raise RuntimeError("Workflow finished without a plan in shared state")

        plan = Plan.model_validate(plan_data)
        results = self._extract_agent_results(state)

        return RunResult(
            run_id=run_id,
            plan_id=plan.plan_id,
            status=state.get("status", "completed"),
            plan=plan,
            results=results,
            memory=memory.load_all(run_id),
        )

    @staticmethod
    def _extract_agent_results(state: dict) -> list[AgentResult]:
        """Collect agent payloads from shared state keys."""
        results: list[AgentResult] = []
        for kind in (
            AgentKind.DISCOVERY,
            AgentKind.VALIDATION,
            AgentKind.CONTACT,
            AgentKind.RECOMMENDATION,
        ):
            data = state.get(kind.value)
            if data:
                results.append(AgentResult(agent=kind, data=data))
        return results
