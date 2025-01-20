from typing import Optional

from wexample_helpers.enums.debug_path_style import DebugPathStyle


def error_format(
    error: Optional[Exception] = None,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    working_directory: Optional[str] = None
) -> None:
    """Format and print an exception with stack trace."""
    from wexample_helpers.helpers.debug import debug_trace

    exc_info = (type(error), error, error.__traceback__)
    debug_trace(
        print_output=True,
        exception_info=exc_info,
        path_style=path_style,
        working_directory=working_directory
    )
