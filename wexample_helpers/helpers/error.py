from typing import Optional, List

from wexample_helpers.enums.debug_path_style import DebugPathStyle
from wexample_helpers.enums.error_truncate_rule import ErrorTruncateRules
from wexample_helpers.helpers.debug import debug_trace, get_traceback_frames
from wexample_helpers.classes.trace_frame import TraceFrame


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
    force_truncate_stack: Optional[int] = None
) -> None:
    if not error:
        return

    exc_info = (type(error), error, error.__traceback__)
    
    if force_truncate_stack is None:
        frames = get_traceback_frames(
            error.__traceback__,
            path_style=path_style,
            working_directory=working_directory
        )
        truncate_index = error_get_truncate_index(frames, error)
        truncate_stack = len(frames) - truncate_index if truncate_index != -1 else 0
    else:
        truncate_stack = force_truncate_stack

    debug_trace(
        print_output=True,
        exception_info=exc_info,
        path_style=path_style,
        working_directory=working_directory,
        truncate_stack=truncate_stack
    )
