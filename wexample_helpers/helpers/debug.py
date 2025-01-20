from types import TracebackType
from typing import List, Optional, TYPE_CHECKING

from wexample_helpers.enums.debug_path_style import DebugPathStyle
from wexample_helpers.helpers.trace import trace_print

if TYPE_CHECKING:
    from wexample_helpers.classes.trace_frame import TraceFrame


def get_traceback_frames(
    traceback: TracebackType,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    working_directory: Optional[str] = None
) -> List["TraceFrame"]:
    """Convert exception traceback frames to TraceFrame objects."""
    from wexample_helpers.classes.trace_frame import TraceFrame

    frames = []
    current = traceback
    while current is not None:
        frame = current.tb_frame
        code = None
        if frame.f_code.co_filename != "<string>":
            try:
                with open(frame.f_code.co_filename, 'r') as f:
                    lines = f.readlines()
                    if 0 <= current.tb_lineno - 1 < len(lines):
                        code = lines[current.tb_lineno - 1]
            except (IOError, IndexError):
                pass

        trace_frame = TraceFrame(
            filename=frame.f_code.co_filename,
            lineno=current.tb_lineno,
            function=frame.f_code.co_name,
            code=code,
            path_style=path_style,
            working_directory=working_directory
        )
        frames.append(trace_frame)
        current = current.tb_next

    return frames


def debug_trace(
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    truncate_stack: int = 0,
    working_directory: Optional[str] = None
) -> None:
    trace_print(
        truncate_stack=truncate_stack,
        path_style=path_style,
        working_directory=working_directory
    )


def debug_trace_and_die(
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    truncate_stack: int = 0,
    working_directory: Optional[str] = None
) -> None:
    debug_trace(
        path_style=path_style,
        truncate_stack=truncate_stack,
        working_directory=working_directory
    )
    exit(1)


def dd() -> None:
    debug_trace_and_die(truncate_stack=2, working_directory=None)
