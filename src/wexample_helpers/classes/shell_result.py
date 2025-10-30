from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ShellResult:
    """Structured result for shell command execution."""

    args: str | list[str]
    cwd: str | None
    duration: float
    end_time: float
    returncode: int
    start_time: float
    stderr: str | None
    stdout: str | None
