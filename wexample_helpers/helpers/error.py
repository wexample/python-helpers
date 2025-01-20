from typing import Optional


def error_format(error: Optional[Exception] = None) -> None:
    """Format and print an exception with stack trace."""
    from wexample_helpers.helpers.debug import debug_trace

    exc_info = (type(error), error, error.__traceback__)
    debug_trace(print_output=True, exception_info=exc_info)
