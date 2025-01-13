from typing import List, Optional, NamedTuple


class TraceFrame(NamedTuple):
    filename: str
    lineno: int
    function: str
    code: Optional[str]

    def __str__(self) -> str:
        base = f"{self.filename}:{self.lineno} in {self.function}"
        if self.code:
            return f"{base}\n  {self.code.strip()}"
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