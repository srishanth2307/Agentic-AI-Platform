# Backend

FastAPI service for the ProspectPilot Agentic AI Platform.

## Layout

| Folder      | Responsibility                          |
|-------------|-----------------------------------------|
| `app/`      | FastAPI factory, middleware, lifespan   |
| `api/`      | HTTP routes and dependencies            |
| `agents/`   | LangGraph agents and graphs             |
| `planner/`  | Goal planning and step decomposition    |
| `tools/`    | Agent-callable tools                    |
| `memory/`   | Checkpoints and retrieval memory        |
| `models/`   | Pydantic schemas and domain types       |
| `database/` | DB engine, ORM, migrations              |
| `config/`   | Environment settings                    |

Run: `uvicorn main:app --reload` from this directory.
