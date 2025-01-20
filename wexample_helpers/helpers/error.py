import inspect
from types import TracebackType
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers.classes.trace_frame import TraceFrame


def error_format(exc_info: Optional[tuple[type[BaseException], BaseException, TracebackType]] = None) -> None:
    """Format and print an exception with stack trace."""
    from wexample_helpers.helpers.debug import debug_trace

    if exc_info is None:
        import sys
        exc_info = sys.exc_info()

    if exc_info[0] is not None:  # If there is an actual exception
        debug_trace(print_output=True, exception_info=exc_info)


def error_get_frames(
    exc_info: tuple[type[BaseException], BaseException, TracebackType],
    short_path: bool = True
) -> List[TraceFrame]:
    from wexample_helpers.classes.trace_frame import TraceFrame

    """Convert exception traceback to TraceFrame objects."""
    frames = []
    tb = exc_info[2]
    while tb:
        frame = tb.tb_frame
        code = None
        try:
            lines = inspect.getsourcelines(frame)[0]
            code = lines[frame.f_lineno - 1]
        except (IOError, OSError):
            pass

        trace_frame = TraceFrame(
            filename=frame.f_code.co_filename,
            lineno=tb.tb_lineno,
            function=frame.f_code.co_name,
            code=code,
            short_path=short_path
        )
        frames.append(trace_frame)
        tb = tb.tb_next

    return frames
