from typing import List, Optional


def debug_trace(print_output: bool = True) -> Optional[List[str]]:
    import inspect
    stack = []

    for frame in inspect.stack()[1:]:
        stack.append(f"{frame.filename}:{frame.lineno}")

    if print_output:
        print('\n'.join(stack))
        return None
    return stack


def debug_trace_and_die() -> None:
    result = debug_trace()
    exit(1)


def dd() -> None:
    debug_trace_and_die()
