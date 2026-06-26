"""Memory layer errors."""


class MemoryKeyNotFoundError(KeyError):
    """Raised when update() targets a key that does not exist."""
