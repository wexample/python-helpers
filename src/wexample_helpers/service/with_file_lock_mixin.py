from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path


class WithFileLockMixin:
    """Mixin adding cross-process file locking via fcntl.flock.

    Combine with any Registry variant (or any class) that performs
    save/load against a shared on-disk resource and may be touched by
    concurrent processes.

    Each operation needing atomicity should wrap its work with
    `with self.file_lock(): ...`. The lock path is derived from the
    backing file's path (suffix ".lock"), or can be overridden via
    `_get_lock_path()`.
    """

    @contextmanager
    def file_lock(self) -> Generator[None]:
        """Acquire an exclusive cross-process lock for the duration of the block."""
        import fcntl

        lock_path = self._get_lock_path()
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with open(lock_path, "w") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                yield
            finally:
                # OS releases the lock when the fd closes; explicit unlock
                # is documented for clarity but not strictly required.
                fcntl.flock(f, fcntl.LOCK_UN)

    def _get_lock_path(self) -> Path:
        """Return the path to the lock file.

        Default implementation derives `.lock` suffix from the backing file's
        path (assumes the host class exposes `_file.path` or similar).
        Subclasses or composing classes should override if the default
        derivation does not apply.
        """
        path = self._get_locked_resource_path()
        return path.with_suffix(path.suffix + ".lock")

    def _get_locked_resource_path(self) -> Path:
        """Path of the resource being protected by the lock. Must be implemented."""
        raise NotImplementedError(
            f"{type(self).__name__} must implement _get_locked_resource_path() "
            "to use WithFileLockMixin"
        )
