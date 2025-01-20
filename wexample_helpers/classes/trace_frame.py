from typing import NamedTuple, Optional
import os

from wexample_helpers.enums.debug_path_style import DebugPathStyle
from wexample_helpers.helpers.cli import cli_make_clickable_path


class TraceFrame(NamedTuple):
    filename: str
    lineno: int
    function: str
    code: Optional[str]
    path_style: DebugPathStyle = DebugPathStyle.FULL
    working_directory: Optional[str] = None

    def get_formatted_path(self) -> str:
        """Get the path according to style and working directory."""
        path = self.filename
        if self.working_directory:
            cwd = os.getcwd()
            if path.startswith(cwd):
                path = os.path.join(self.working_directory, os.path.relpath(path, cwd))

        if self.path_style == DebugPathStyle.FULL:
            return path
        elif self.path_style == DebugPathStyle.RELATIVE:
            try:
                return os.path.relpath(path)
            except ValueError:
                return path
        else:
            return os.path.basename(path)

    def format_frame(self) -> str:
        formatted_path = self.get_formatted_path()
        path_with_line = f"{formatted_path}:{self.lineno}"
        
        base = (
            f"\n{'-' * 50}\n"
            f"File     : {cli_make_clickable_path(path_with_line)}\n"
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
