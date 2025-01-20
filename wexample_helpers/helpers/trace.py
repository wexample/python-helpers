from typing import List, TYPE_CHECKING, Optional

from wexample_helpers.enums.debug_path_style import DebugPathStyle

if TYPE_CHECKING:
    from wexample_helpers.classes.trace_frame import TraceFrame


def trace_print(
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    truncate_stack: int = 0,
    working_directory: Optional[str] = None
) -> None:
    print(trace_format(
        trace_get_frames(
            skip_frames=truncate_stack,
            path_style=path_style,
            working_directory=working_directory
        )
    ))


def trace_get_frames(
    skip_frames: int = 0,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    working_directory: Optional[str] = None
) -> List["TraceFrame"]:
    import inspect
    """Convert stack frames to TraceFrame objects."""
    from wexample_helpers.classes.trace_frame import TraceFrame

    frames = []
    for frame in inspect.stack()[1 + skip_frames:]:
        trace_frame = TraceFrame(
            filename=frame.filename,
            lineno=frame.lineno,
            function=frame.function,
            code=frame.code_context[0] if frame.code_context else None,
            path_style=path_style,
            working_directory=working_directory
        )
        frames.append(trace_frame)

    frames.reverse()
    return frames


def trace_format(
    traceback_frames: List["TraceFrame"]
) -> str:
    """Format a list of TraceFrame objects and optional exception information."""
    parts = [str(frame) for frame in traceback_frames]

    return '\n'.join(parts)
