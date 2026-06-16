from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.enums.debug_path_style import DebugPathStyle

if TYPE_CHECKING:
    # Backward-compat type alias to new frame class; TraceFrame is not exported
    # separately from frame.py, so keep only the aliased import.
    from wexample_helpers.common.exception.frame import ExceptionFrame as TraceFrame

# Module-level singleton — ExceptionHandler and its TraceFormatter are stateless;
# reusing one instance eliminates per-call constructor overhead.
_handler = None


def _get_handler():
    global _handler
    if _handler is None:
        from wexample_helpers.common.exception.handler import ExceptionHandler

        _handler = ExceptionHandler()
    return _handler


def error_format(
    error: Exception | None = None,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    paths_map: dict | None = None,
) -> str:
    return _get_handler().format_exception(
        error,
        path_style=path_style,
        paths_map=paths_map,
    )


def error_get_truncate_index(frames: list[TraceFrame], error: Exception) -> int:
    """Returns the index where to truncate the trace based on error type. Returns -1 if no truncation needed."""
    # Delegate to ExceptionHandler internals to avoid duplication, but keep public API.
    return _get_handler()._get_truncate_index(frames, error)  # type: ignore[attr-defined]
