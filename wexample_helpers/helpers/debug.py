import inspect
from types import TracebackType
from typing import List, Optional, TYPE_CHECKING

from wexample_helpers.enums.debug_path_style import DebugPathStyle

if TYPE_CHECKING:
    from wexample_helpers.classes.trace_frame import TraceFrame


def get_traceback_frames(
    traceback: TracebackType,
    path_style: DebugPathStyle = DebugPathStyle.FULL
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
            path_style=path_style
        )
        frames.append(trace_frame)
        current = current.tb_next

    return frames


def get_stack_frames(
    skip_frames: int = 0,
    path_style: DebugPathStyle = DebugPathStyle.FULL
) -> List["TraceFrame"]:
    """Convert stack frames to TraceFrame objects."""
    from wexample_helpers.classes.trace_frame import TraceFrame

    frames = []
    for frame in inspect.stack()[1 + skip_frames:]:
        trace_frame = TraceFrame(
            filename=frame.filename,
            lineno=frame.lineno,
            function=frame.function,
            code=frame.code_context[0] if frame.code_context else None,
            path_style=path_style
        )
        frames.append(trace_frame)

    frames.reverse()
    return frames


def debug_trace(
    print_output: bool = True,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    truncate_stack: int = 0,
    exception_info: Optional[tuple[type[BaseException], BaseException, TracebackType]] = None
) -> Optional[List["TraceFrame"]]:
    """
    Trace l'exécution du code avec différentes options de formatage des chemins.
    
    Args:
        print_output: Si True, affiche la trace. Sinon, retourne les frames.
        path_style: Style d'affichage des chemins ("full", "relative", "filename")
        truncate_stack: Nombre de frames à ignorer au début de la stack
        exception_info: Informations sur l'exception si applicable
    """
    from wexample_helpers.helpers.trace import trace_format

    if exception_info and exception_info[2]:
        frames = get_traceback_frames(exception_info[2], path_style)
    else:
        frames = get_stack_frames(truncate_stack, path_style)

    if print_output:
        print(trace_format(frames, exception_info))
        return None
    return frames


def debug_trace_and_die(path_style: DebugPathStyle = DebugPathStyle.FULL, truncate_stack: int = 0) -> None:
    debug_trace(path_style=path_style, truncate_stack=truncate_stack)
    exit(1)


def dd() -> None:
    debug_trace_and_die(truncate_stack=2)
