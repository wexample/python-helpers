from types import TracebackType
from typing import List, TYPE_CHECKING, Optional

from wexample_helpers.enums.debug_path_style import DebugPathStyle

if TYPE_CHECKING:
    # Backward-compat type alias to new frame class
    from wexample_helpers.common.exception.frame import ExceptionFrame as TraceFrame

from wexample_helpers.common.exception.collector import TraceCollector
from wexample_helpers.common.exception.formatter import TraceFormatter


def trace_print(
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    truncate_stack: int = 0,
    paths_map: Optional[dict] = None
) -> None:
    print(
        trace_format(
            trace_get_frames(
                skip_frames=truncate_stack,
                path_style=path_style,
                paths_map=paths_map,
            )
        )
    )


def trace_get_traceback_frames(
    traceback: TracebackType,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    paths_map: Optional[dict] = None
) -> List["TraceFrame"]:
    """Convert exception traceback frames to TraceFrame objects."""
    return TraceCollector.from_traceback(
        traceback,
        path_style=path_style,
        paths_map=paths_map,
    )


def trace_get_frames(
    skip_frames: int = 0,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    paths_map: Optional[dict] = None
) -> List["TraceFrame"]:
    """Convert stack frames to TraceFrame objects."""
    return TraceCollector.from_stack(
        skip_frames=skip_frames,
        path_style=path_style,
        paths_map=paths_map,
    )


def trace_format(
    traceback_frames: List["TraceFrame"]
) -> str:
    """Format a list of TraceFrame objects and optional exception information."""
    return TraceFormatter().format(traceback_frames)
