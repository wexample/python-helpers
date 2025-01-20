from typing import Optional, List, Dict

from wexample_helpers.classes.trace_frame import TraceFrame
from wexample_helpers.enums.debug_path_style import DebugPathStyle
from wexample_helpers.enums.error_truncate_rule import ErrorTruncateRules
from wexample_helpers.helpers.debug import get_traceback_frames


def error_get_truncate_index(frames: List[TraceFrame], error: Exception) -> int:
    """Returns the index where to truncate the trace based on error type. Returns -1 if no truncation needed."""
    error_module = error.__class__.__module__

    for rule_type in ErrorTruncateRules:
        if error_module.startswith(rule_type.module_prefix):
            rule = rule_type.rule

            if rule.truncate_stack_count is not None:
                return min(rule.truncate_stack_count, len(frames))

            for i, frame in enumerate(frames):
                filename = frame.filename

                if rule.truncate_after_module and rule.truncate_after_module in filename:
                    return i + 1

                if rule.truncate_after_file and filename.endswith(rule.truncate_after_file):
                    return i + 1

    return -1


def error_format(
    error: Optional[Exception] = None,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    paths_map: Optional[Dict[str, str]] = None,
) -> None:
    if not error:
        return

    from wexample_helpers.helpers.trace import trace_print, trace_format
    
    # Get frames from the exception traceback
    frames = get_traceback_frames(
        error.__traceback__,
        path_style=path_style,
        paths_map=paths_map
from typing import Optional, List

from wexample_helpers.classes.trace_frame import TraceFrame
from wexample_helpers.enums.debug_path_style import DebugPathStyle
from wexample_helpers.enums.error_truncate_rule import ErrorTruncateRules
from wexample_helpers.helpers.debug import get_traceback_frames


def error_get_truncate_index(frames: List[TraceFrame], error: Exception) -> int:
    """Returns the index where to truncate the trace based on error type. Returns -1 if no truncation needed."""
    error_module = error.__class__.__module__

    for rule_type in ErrorTruncateRules:
        if error_module.startswith(rule_type.module_prefix):
            rule = rule_type.rule

            if rule.truncate_stack_count is not None:
                return min(rule.truncate_stack_count, len(frames))

            for i, frame in enumerate(frames):
                filename = frame.filename

                if rule.truncate_after_module and rule.truncate_after_module in filename:
                    return i + 1

                if rule.truncate_after_file and filename.endswith(rule.truncate_after_file):
                    return i + 1

    return -1


def error_format(
    error: Optional[Exception] = None,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    working_directory: Optional[str] = None,
) -> None:
    if not error:
        return

    from wexample_helpers.helpers.trace import trace_print

    frames = get_traceback_frames(
        error.__traceback__,
        path_style=path_style,
        working_directory=working_directory
    )
    truncate_index = error_get_truncate_index(frames, error)
    truncate_stack = len(frames) - truncate_index if truncate_index != -1 else 0

    trace_print(
        truncate_stack=truncate_stack,
        path_style=path_style,
        working_directory=working_directory
    )
