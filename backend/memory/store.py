"""SQLite-backed shared memory — key/value store scoped by run_id."""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from memory.exceptions import MemoryKeyNotFoundError

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS memory_entries (
    run_id   TEXT NOT NULL,
    key      TEXT NOT NULL,
    value    TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (run_id, key)
)
"""


class SharedMemoryStore:
    """Persists run-scoped data agents can read and write."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(_CREATE_TABLE)

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _serialize(value: Any) -> str:
        return json.dumps(value)

    @staticmethod
    def _deserialize(raw: str) -> Any:
        return json.loads(raw)

    def save(self, run_id: str, key: str, value: Any) -> None:
        """Insert or replace a value for (run_id, key)."""
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO memory_entries (run_id, key, value, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(run_id, key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at
                """,
                (run_id, key, self._serialize(value), self._now()),
            )

    def load(self, run_id: str, key: str, default: Any = None) -> Any:
        """Return a stored value, or default if the key is missing."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT value FROM memory_entries WHERE run_id = ? AND key = ?",
                (run_id, key),
            ).fetchone()
        if row is None:
            return default
        return self._deserialize(row["value"])

    def load_all(self, run_id: str) -> dict[str, Any]:
        """Return every key/value pair for a run — used to build agent context."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT key, value FROM memory_entries WHERE run_id = ?",
                (run_id,),
            ).fetchall()
        return {row["key"]: self._deserialize(row["value"]) for row in rows}

    def update(self, run_id: str, key: str, value: Any) -> None:
        """Replace a value only if the key already exists."""
        with self._connect() as conn:
            cursor = conn.execute(
                """
                UPDATE memory_entries
                SET value = ?, updated_at = ?
                WHERE run_id = ? AND key = ?
                """,
                (self._serialize(value), self._now(), run_id, key),
            )
        if cursor.rowcount == 0:
            raise MemoryKeyNotFoundError(f"No entry for run_id={run_id!r}, key={key!r}")

    def delete(self, run_id: str, key: str) -> bool:
        """Remove a key. Returns True if a row was deleted."""
        with self._connect() as conn:
            cursor = conn.execute(
                "DELETE FROM memory_entries WHERE run_id = ? AND key = ?",
                (run_id, key),
            )
        return cursor.rowcount > 0

    def delete_run(self, run_id: str) -> int:
        """Remove all keys for a run. Returns number of rows deleted."""
        with self._connect() as conn:
            cursor = conn.execute(
                "DELETE FROM memory_entries WHERE run_id = ?",
                (run_id,),
            )
        return cursor.rowcount
