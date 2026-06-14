from __future__ import annotations

import inspect
import linecache
from typing import TYPE_CHECKING

from wexample_helpers.enums.debug_path_style import DebugPathStyle

if TYPE_CHECKING:
    from types import TracebackType

    from wexample_helpers.common.exception.frame import ExceptionFrame


class TraceCollector:
    """Collects frames from current stack or from an exception traceback."""

    @staticmethod
    def from_stack(
        *,
        path_style: DebugPathStyle = DebugPathStyle.FULL,
        paths_map: dict[str, str] | None = None,
    ) -> list[ExceptionFrame]:
        from wexample_helpers.common.exception.frame import ExceptionFrame

        frames: list[ExceptionFrame] = []
        # Skip only from_stack itself (frame 0)
        for frame in inspect.stack()[1:]:
            is_internal = TraceCollector._is_internal_frame(frame.filename)
            # inspect.stack() defaults to context=1, so code_context is at most
            # a 1-element list — index directly instead of allocating a join.
            code = frame.code_context[0] if frame.code_context else None
            frames.append(
                ExceptionFrame(
                    filename=frame.filename,
                    lineno=frame.lineno,
                    function=frame.function,
                    code=code,
                    path_style=path_style,
                    paths_map=paths_map,
                    is_internal=is_internal,
                )
            )
        frames.reverse()
        return frames

    @staticmethod
    def from_traceback(
        traceback: TracebackType,
        *,
        path_style: DebugPathStyle = DebugPathStyle.FULL,
        paths_map: dict[str, str] | None = None,
    ) -> list[ExceptionFrame]:
        from wexample_helpers.common.exception.frame import ExceptionFrame

        frames: list[ExceptionFrame] = []
        current = traceback
        while current is not None:
            frame = current.tb_frame
            f_code = frame.f_code
            filename = f_code.co_filename
            # linecache caches file contents keyed by filename, so repeated
            # frames from the same file are served from memory rather than
            # triggering a fresh full-file read each time.  It also handles
            # synthetic filenames (e.g. "<string>") and missing files
            # gracefully by returning "".
            code = linecache.getline(filename, current.tb_lineno) or None

            is_internal = TraceCollector._is_internal_frame(filename)
            frames.append(
                ExceptionFrame(
                    filename=filename,
                    lineno=current.tb_lineno,
                    function=f_code.co_name,
                    code=code,
                    path_style=path_style,
                    paths_map=paths_map,
                    is_internal=is_internal,
                )
            )
            current = current.tb_next
        return frames

    @staticmethod
    def _is_internal_frame(filename: str) -> bool:
        """Check if a frame is from internal debug/trace helpers."""
        return filename.endswith(("/helpers/trace.py", "/helpers/debug.py"))
