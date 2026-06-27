"""Invokes the LangGraph workflow and returns final shared state."""

from datetime import datetime, timezone
from uuid import uuid4

import memory
from graph.state import WorkflowState
from graph.workflow import get_workflow
from models.business_config import BusinessConfiguration, default_business_config

# Sequential LangGraph node order — used for progress calculation
_NODE_ORDER = ["planner", "discovery", "validation", "contact", "recommendation"]


class WorkflowRunner:
    """
    Bridges RunService and LangGraph.

    Builds initial state, invokes the compiled graph, and relies on node-level
    persistence to keep SQLite memory in sync.
    """

    def run(
        self,
        goal: str,
        business_config: BusinessConfiguration | None = None,
        run_id: str | None = None,
    ) -> WorkflowState:
        run_id = run_id or str(uuid4())
        config = business_config or default_business_config()

        # Seed shared state — LangGraph merges node updates into this dict
        initial_state: WorkflowState = {
            "run_id": run_id,
            "goal": goal,
            "business_config": config.model_dump(mode="json"),
            "status": "planning",
            "current_agent": "pending",
            "errors": [],
        }

        # Persist inputs before the graph runs
        memory.save(run_id, "goal", goal)
        memory.save(run_id, "business_config", config.model_dump(mode="json"))
        memory.save(run_id, "status", "planning")

        workflow = get_workflow()
        final_state: WorkflowState = workflow.invoke(initial_state)

        memory.save(run_id, "status", final_state.get("status", "completed"))
        return final_state

    def stream(
        self,
        goal: str,
        business_config: BusinessConfiguration | None = None,
        run_id: str | None = None,
    ):
        """
        Yield SSE progress events as each LangGraph node completes.

        Emits agent started/completed events with live memory snapshots.
        """
        run_id = run_id or str(uuid4())
        config = business_config or default_business_config()

        initial_state: WorkflowState = {
            "run_id": run_id,
            "goal": goal,
            "business_config": config.model_dump(mode="json"),
            "status": "planning",
            "current_agent": "pending",
            "errors": [],
        }

        memory.save(run_id, "goal", goal)
        memory.save(run_id, "business_config", config.model_dump(mode="json"))
        memory.save(run_id, "status", "planning")

        accumulated: dict = dict(initial_state)
        workflow = get_workflow()

        # Real start signal — planner is the first LangGraph node
        yield self._sse_event(
            "planner_started",
            run_id,
            agent="planner",
            status="started",
            progress=self._progress("planner", "started"),
            memory=memory.load_all(run_id),
        )

        for chunk in workflow.stream(initial_state, stream_mode="updates"):
            for node_name, update in chunk.items():
                if node_name not in _NODE_ORDER:
                    continue

                accumulated.update(update)
                memory.save(run_id, "status", accumulated.get("status", "executing"))
                snap = memory.load_all(run_id)
                output = self._agent_output(node_name, update, accumulated)

                yield self._sse_event(
                    f"{node_name}_completed",
                    run_id,
                    agent=node_name,
                    status="completed",
                    progress=self._progress(node_name, "completed"),
                    memory=snap,
                    output=output,
                )

                yield self._sse_event(
                    "memory_updated",
                    run_id,
                    agent=node_name,
                    status="updated",
                    progress=self._progress(node_name, "completed"),
                    memory=snap,
                    output=output,
                )

                next_agent = self._next_agent(node_name)
                if next_agent:
                    yield self._sse_event(
                        f"{next_agent}_started",
                        run_id,
                        agent=next_agent,
                        status="started",
                        progress=self._progress(next_agent, "started"),
                        memory=snap,
                    )

        memory.save(run_id, "status", accumulated.get("status", "completed"))
        yield {
            "event": "run_completed",
            "timestamp": self._timestamp(),
            "run_id": run_id,
            "agent": "done",
            "status": "completed",
            "progress": 100,
            "memory": memory.load_all(run_id),
            "state": accumulated,
        }

    @staticmethod
    def _timestamp() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _progress(agent: str, phase: str) -> int:
        idx = _NODE_ORDER.index(agent)
        base = idx * 20
        return base if phase == "started" else base + 20

    @staticmethod
    def _next_agent(current: str) -> str | None:
        idx = _NODE_ORDER.index(current)
        if idx + 1 < len(_NODE_ORDER):
            return _NODE_ORDER[idx + 1]
        return None

    @staticmethod
    def _agent_output(node_name: str, update: dict, accumulated: dict):
        if node_name == "planner":
            return update.get("plan") or accumulated.get("plan")
        return update.get(node_name) or accumulated.get(node_name)

    @classmethod
    def _sse_event(
        cls,
        event: str,
        run_id: str,
        *,
        agent: str,
        status: str,
        progress: int,
        memory: dict | None = None,
        output=None,
    ) -> dict:
        payload = {
            "event": event,
            "timestamp": cls._timestamp(),
            "run_id": run_id,
            "agent": agent,
            "status": status,
            "progress": progress,
        }
        if memory is not None:
            payload["memory"] = memory
        if output is not None:
            payload["output"] = output
        return payload
