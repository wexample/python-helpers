import inspect
from types import TracebackType
from typing import List, Optional, TYPE_CHECKING

from wexample_helpers.enums.debug_path_style import DebugPathStyle

if TYPE_CHECKING:
    from wexample_helpers.classes.trace_frame import TraceFrame


def get_stack_frames(
    skip_frames: int = 0,
    path_style: DebugPathStyle = DebugPathStyle.RELATIVE
) -> List["TraceFrame"]:
    from wexample_helpers.classes.trace_frame import TraceFrame

    """Convert stack frames to TraceFrame objects."""
    frames = []
    for frame in inspect.stack()[1 + skip_frames:]:
        trace_frame = TraceFrame(
            filename=frame.filename,
            lineno=frame.lineno,
            function=frame.function,
            code=frame.code_context[0] if frame.code_context else None,
            path_style=path_style
        )
        frames.append(trace_frame)

    frames.reverse()
    return frames


def debug_trace(
    print_output: bool = True,
    path_style: DebugPathStyle = DebugPathStyle.RELATIVE,
    truncate_stack: int = 0,
    exception_info: Optional[tuple[type[BaseException], BaseException, TracebackType]] = None
) -> Optional[List["TraceFrame"]]:
    from wexample_helpers.helpers.trace import trace_format
    frames = get_stack_frames(truncate_stack, path_style)

    if print_output:
        print(trace_format(frames, exception_info))
        return None
    return frames


def debug_trace_and_die(path_style: DebugPathStyle = DebugPathStyle.RELATIVE, truncate_stack: int = 0) -> None:
    debug_trace(path_style=path_style, truncate_stack=truncate_stack)
    exit(1)


def dd() -> None:
    debug_trace_and_die(truncate_stack=2)
