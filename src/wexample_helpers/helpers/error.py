from __future__ import annotations

from functools import cache
from typing import TYPE_CHECKING

from wexample_helpers.enums.debug_path_style import DebugPathStyle

if TYPE_CHECKING:
    # Backward-compat type alias to new frame class; TraceFrame is not exported
    # separately from frame.py, so keep only the aliased import.
    from wexample_helpers.common.exception.frame import ExceptionFrame as TraceFrame


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


@cache
def _get_handler():
    # @cache (C-level) replaces the manual global+None-check pattern;
    # ExceptionHandler and its TraceFormatter are stateless so a single
    # instance is safe to reuse across all callers.
    from wexample_helpers.common.exception.handler import ExceptionHandler

    return ExceptionHandler()
