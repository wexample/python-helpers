import os
from typing import NamedTuple, Optional

from wexample_helpers.enums.debug_path_style import DebugPathStyle
from wexample_helpers.helpers.cli import cli_make_clickable_path


class TraceFrame(NamedTuple):
    filename: str
    lineno: int
    function: str
    code: Optional[str]
    path_style: DebugPathStyle = DebugPathStyle.FULL

    def get_formatted_path(self) -> str:
        if self.path_style == DebugPathStyle.FULL:
            return self.filename
        elif self.path_style == DebugPathStyle.RELATIVE:
            try:
                return os.path.relpath(self.filename)
            except ValueError:
                return self.filename
        else:
            return self.filename

    def format_frame(self) -> str:
        path_with_line = f"{self.filename}:{self.lineno}"
        # Format the base information
        base = (
            f"\n{'-' * 50}\n"
            f"File     : {cli_make_clickable_path(path_with_line, short_title=self.get_formatted_path())}\n"
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
