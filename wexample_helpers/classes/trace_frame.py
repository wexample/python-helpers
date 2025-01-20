from typing import NamedTuple, Optional

from wexample_helpers.helpers.cli import cli_make_clickable_path


class TraceFrame(NamedTuple):
    filename: str
    lineno: int
    function: str
    code: Optional[str]
    short_path: bool

    def format_frame(self) -> str:
        path_with_line = f"{self.filename}:{self.lineno}"
        # Format the base information
        base = (
            f"\n{'-' * 50}\n"
            f"File     : {cli_make_clickable_path(path_with_line, short_title=self.short_path)}\n"
            f"Line     : {self.lineno}\n"
            f"Function : {self.function}"
        )

        # Add code context if available
        if self.code:
            code_section = f"\nCode     : {self.code.strip()}"
            return f"{base}{code_section}"
        return base

    def __str__(self) -> str:
        return self.format_frame()
