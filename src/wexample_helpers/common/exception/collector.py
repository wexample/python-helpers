from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

from wexample_helpers.common.exception.frame import ExceptionFrame
from wexample_helpers.enums.debug_path_style import DebugPathStyle

if TYPE_CHECKING:
    from types import TracebackType


class TraceCollector:
    """Collects frames from current stack or from an exception traceback."""

    @staticmethod
    def _is_internal_frame(filename: str) -> bool:
        """Check if a frame is from internal debug/trace helpers."""
        return filename.endswith(("/helpers/trace.py", "/helpers/debug.py"))

    @staticmethod
    def from_stack(
            *,
            skip_frames: int | None = None,
            path_style: DebugPathStyle = DebugPathStyle.FULL,
            paths_map: dict[str, str] | None = None,
    ) -> list[ExceptionFrame]:
        frames: list[ExceptionFrame] = []
        for frame in inspect.stack()[
                     (skip_frames + 1 if skip_frames is not None else 0):
                     ]:
            is_internal = TraceCollector._is_internal_frame(frame.filename)
            # Join all code context lines if available
            code = "".join(frame.code_context) if frame.code_context else None
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
        frames: list[ExceptionFrame] = []
        current = traceback
        while current is not None:
            frame = current.tb_frame
            code = None
            if frame.f_code.co_filename != "<string>":
                try:
                    with open(frame.f_code.co_filename) as f:
                        lines = f.readlines()
                        if 0 <= current.tb_lineno - 1 < len(lines):
                            code = lines[current.tb_lineno - 1]
                except (OSError, IndexError):
                    pass

            is_internal = TraceCollector._is_internal_frame(frame.f_code.co_filename)
            frames.append(
                ExceptionFrame(
                    filename=frame.f_code.co_filename,
                    lineno=current.tb_lineno,
                    function=frame.f_code.co_name,
                    code=code,
                    path_style=path_style,
                    paths_map=paths_map,
                    is_internal=is_internal,
                )
            )
            current = current.tb_next
        return frames
