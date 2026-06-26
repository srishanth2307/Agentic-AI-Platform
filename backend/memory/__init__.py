"""Shared memory — SQLite key/value store scoped by run_id."""

from memory.exceptions import MemoryKeyNotFoundError
from memory.store import SharedMemoryStore

_default_store: SharedMemoryStore | None = None


def _get_store() -> SharedMemoryStore:
    global _default_store
    if _default_store is None:
        from config.settings import settings

        _default_store = SharedMemoryStore(settings.memory_db_path)
    return _default_store


def save(run_id: str, key: str, value: object) -> None:
    """Insert or replace a value for (run_id, key)."""
    _get_store().save(run_id, key, value)


def load(run_id: str, key: str, default: object = None) -> object:
    """Return a stored value, or default if the key is missing."""
    return _get_store().load(run_id, key, default)


def load_all(run_id: str) -> dict[str, object]:
    """Return every key/value pair for a run."""
    return _get_store().load_all(run_id)


def update(run_id: str, key: str, value: object) -> None:
    """Replace a value only if the key already exists."""
    _get_store().update(run_id, key, value)


def delete(run_id: str, key: str) -> bool:
    """Remove a key. Returns True if a row was deleted."""
    return _get_store().delete(run_id, key)


__all__ = [
    "MemoryKeyNotFoundError",
    "SharedMemoryStore",
    "delete",
    "load",
    "load_all",
    "save",
    "update",
]
