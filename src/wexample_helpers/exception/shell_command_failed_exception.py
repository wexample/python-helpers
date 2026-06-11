from __future__ import annotations

from typing import ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.exception.undefined_exception import UndefinedException


@base_class
class ShellCommandFailedException(UndefinedException):
    error_code: ClassVar[str] = "SHELL_COMMAND_FAILED"

    cmd: list[str] | str = public_field(description="Command that was executed")
    returncode: int = public_field(description="Exit code returned by the command")
    stderr: str | None = public_field(
        default=None, description="Standard error output of the command"
    )
    stdout: str | None = public_field(
        default=None, description="Standard output of the command"
    )

    def _build_message(self) -> str:
        return f"Command exited with code {self.returncode}"
