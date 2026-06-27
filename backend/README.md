# Backend

FastAPI + LangGraph service for the ProspectPilot Agentic AI Platform.

## Layout

| Folder      | Responsibility                                      |
|-------------|-----------------------------------------------------|
| `app/`      | FastAPI factory, middleware, lifespan               |
| `api/`      | HTTP routes and dependencies                        |
| `graph/`    | LangGraph workflow, nodes, shared state, persistence |
| `planner/`  | Planner + PlannerAgent (ICP-aware planning)         |
| `agents/`   | Reusable agent classes (read/write shared state)    |
| `services/` | RunService, WorkflowRunner orchestration              |
| `memory/`   | SQLite shared memory                                |
| `models/`   | Pydantic schemas (incl. BusinessConfiguration)      |
| `config/`   | Environment settings                                |

## Workflow

```
POST /api/v1/runs → RunService → LangGraph:
  Planner → Discovery → Validation → Contact → Recommendation
```

Each node updates `WorkflowState` and persists to SQLite memory.

Run: `uvicorn main:app --reload` from this directory.
