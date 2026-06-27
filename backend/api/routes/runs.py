"""Run execution endpoints."""

import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models.run import RunRequest, RunResponse
from services.run_service import RunService

router = APIRouter(prefix="/runs", tags=["runs"])

_run_service = RunService()


@router.post("", response_model=RunResponse)
def create_run(request: RunRequest) -> RunResponse:
    """
    Start a LangGraph agent run (blocking):

    Planner → Discovery → Validation → Contact → Recommendation → Memory → JSON
    """
    return _run_service.execute(request)


@router.post("/stream")
def stream_run(request: RunRequest) -> StreamingResponse:
    """Stream real agent progress events for the live dashboard (SSE)."""

    def event_generator():
        try:
            for event in _run_service.stream(request):
                event_name = event.get("event", "message")
                yield f"event: {event_name}\ndata: {json.dumps(event, default=str)}\n\n"
        except Exception as exc:
            failed = {
                "event": "run_failed",
                "error": str(exc),
                "status": "failed",
            }
            yield f"event: run_failed\ndata: {json.dumps(failed, default=str)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
