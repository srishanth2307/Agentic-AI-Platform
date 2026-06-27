"""HTTP API layer — route handlers and dependencies."""

from fastapi import APIRouter

from api.routes.runs import router as runs_router

api_router = APIRouter()
api_router.include_router(runs_router)
