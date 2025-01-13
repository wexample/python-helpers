from typing import List, Optional, NamedTuple

from wexample_helpers.helpers.cli import cli_make_clickable_path


class TraceFrame(NamedTuple):
    filename: str
    lineno: int
    function: str
    code: Optional[str]
    short_path: bool

    def __str__(self) -> str:
        # Format the base information
        base = (
            f"\n{'-' * 50}\n"
            f"File     : {cli_make_clickable_path(self.filename, short_title=self.short_path)}:{self.lineno}\n"
            f"Line     : {self.lineno}\n"
            f"Function : {self.function}"
        )

        # Add code context if available
        if self.code:
            code_section = (
                f"\nCode     : {self.code.strip()}"
            )
            return f"{base}{code_section}"
        return base


def debug_trace(print_output: bool = True, short_path: bool = True) -> Optional[List[TraceFrame]]:
    import inspect
    stack = []

    for frame in inspect.stack()[1:]:
        trace_frame = TraceFrame(
            filename=frame.filename,
            lineno=frame.lineno,
            function=frame.function,
            code=frame.code_context[0] if frame.code_context else None,
            short_path=short_path
        )
        stack.append(trace_frame)

    if print_output:
        print('\n'.join(str(frame) for frame in stack))
        return None
    return stack


def debug_trace_and_die(short_path: bool = True) -> None:
    debug_trace(short_path=short_path)
    exit(1)


def dd() -> None:
    debug_trace_and_die()
