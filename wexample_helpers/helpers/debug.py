from typing import Optional, TYPE_CHECKING

from wexample_helpers.enums.debug_path_style import DebugPathStyle
from wexample_helpers.helpers.trace import trace_print

if TYPE_CHECKING:
    pass


def debug_trace(
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    truncate_stack: int = 0,
    paths_map: Optional[dict] = None
) -> None:
    trace_print(
        truncate_stack=truncate_stack,
        path_style=path_style,
        paths_map=paths_map
    )


def debug_trace_and_die(
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    truncate_stack: int = 0,
    paths_map: Optional[dict] = None,
    message: str = None
) -> None:
    if message:
        print(f"\n {message}")
    
    debug_trace(
        path_style=path_style,
        truncate_stack=truncate_stack,
        paths_map=paths_map
    )
    exit(1)


def dd(message: str = None) -> None:
    """
    Debug and die - prints a message and exits
    """
    if message:
        print(f"\n {message}")
    exit(1)


def debug_breakpoint(message: str = None) -> None:
    if message:
        print(f"\n Debug breakpoint: {message}")
        print("Commands:")
        print("  p variable  : Print variable")
        print("  n          : Next line")
        print("  c          : Continue execution")
        print("  q          : Quit")
        print("  h          : Help (more commands)")
    
    import pdb
    pdb.set_trace()
