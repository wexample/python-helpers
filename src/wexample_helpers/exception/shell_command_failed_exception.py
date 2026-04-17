from __future__ import annotations

import shlex
from typing import Any

from wexample_helpers.exception.undefined_exception import UndefinedException


class ShellCommandFailedException(UndefinedException):
    error_code: str = "SHELL_COMMAND_FAILED"

    def __init__(
        self,
        cmd: list[str] | str,
        returncode: int,
        stderr: str | None = None,
        stdout: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        self.cmd = cmd
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = stdout

        cmd_str = shlex.join(cmd) if isinstance(cmd, list) else cmd
        data: dict[str, Any] = {"command": cmd_str, "returncode": returncode}
        if stderr and stderr.strip():
            data["stderr"] = stderr.strip()

        super().__init__(
            message=f"Command exited with code {returncode}",
            data=data,
            cause=cause,
        )
