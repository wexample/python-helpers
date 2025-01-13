from typing import List, Optional, NamedTuple
import os


class TraceFrame(NamedTuple):
    filename: str
    lineno: int
    function: str
    code: Optional[str]

    def __str__(self) -> str:
        # Format the base information
        base = (
            f"\n{'-' * 50}\n"
            f"File     : {self.filename}\n"
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


def debug_trace(print_output: bool = True) -> Optional[List[TraceFrame]]:
    import inspect
    stack = []

    for frame in inspect.stack()[1:]:
        trace_frame = TraceFrame(
            filename=frame.filename,
            lineno=frame.lineno,
            function=frame.function,
            code=frame.code_context[0] if frame.code_context else None
        )
        stack.append(trace_frame)

    if print_output:
        print('\n'.join(str(frame) for frame in stack))
        return None
    return stack


def debug_trace_and_die() -> None:
    result = debug_trace()
    exit(1)


def dd() -> None:
    debug_trace_and_die()