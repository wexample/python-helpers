from types import TracebackType
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from wexample_helpers.classes.trace_frame import TraceFrame


def trace_format(
    traceback_frames: List["TraceFrame"],
    exception_info: Optional[tuple[type[BaseException], BaseException, TracebackType]] = None
) -> str:
    """Format a list of TraceFrame objects and optional exception information."""
    parts = [str(frame) for frame in traceback_frames]

    if exception_info:
        exc_type, exc_value, _ = exception_info
        parts.append(f"\n{'-' * 50}")
        parts.append(f"Exception: {exc_type.__name__}: {str(exc_value)}")

    return '\n'.join(parts)