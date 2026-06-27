"""Persist workflow state slices to SQLite shared memory after each node."""

import memory

# Keys mirrored to durable storage for dashboard / resume support
_PERSISTED_KEYS = frozenset({
    "goal",
    "business_config",
    "plan",
    "discovery",
    "validation",
    "contact",
    "recommendation",
    "status",
    "current_agent",
})


def persist_state_update(run_id: str, update: dict) -> None:
    """Write relevant state keys to shared memory after a node completes."""
    for key, value in update.items():
        if key in _PERSISTED_KEYS:
            memory.save(run_id, key, value)
