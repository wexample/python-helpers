import inspect
from typing import Any
from typing import Optional, TYPE_CHECKING

from colorama import Fore, Style

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


def debug_dump(obj: Any, max_depth: int = 100, _depth: int = 0, _seen=None) -> None:
    if _seen is None:
        _seen = set()

    if _depth > max_depth:
        print(f"{' ' * _depth}{Fore.YELLOW}[Max depth reached]{Style.RESET_ALL}")
        return

    obj_id = id(obj)
    if obj_id in _seen and not isinstance(obj, (int, float, str, bool)):
        print(f"{' ' * _depth}{Fore.YELLOW}[Circular reference]{Style.RESET_ALL}")
        return
    _seen.add(obj_id)

    indent = ' ' * _depth
    obj_type = type(obj).__name__

    type_str = f"{Fore.BLUE}{obj_type}{Style.RESET_ALL}"

    if obj is None:
        print(f"{indent}{type_str}: {Style.BRIGHT}None{Style.RESET_ALL}")

    elif isinstance(obj, (int, float, str, bool)):
        print(f"{indent}{type_str}: {Fore.GREEN}{repr(obj)}{Style.RESET_ALL}")

    elif isinstance(obj, (list, tuple)):
        print(f"{indent}{type_str} ({len(obj)} elements):")
        for i, item in enumerate(obj):
            print(f"{indent}  {Style.BRIGHT}[{i}]{Style.RESET_ALL} →")
            debug_dump(item, max_depth, _depth + 4, _seen)

    elif isinstance(obj, dict):
        print(f"{indent}{type_str} ({len(obj)} elements):")
        for key, value in obj.items():
            print(f"{indent}  {Style.BRIGHT}{repr(key)}{Style.RESET_ALL} →")
            debug_dump(value, max_depth, _depth + 4, _seen)

    elif inspect.isfunction(obj) or inspect.ismethod(obj):
        print(f"{indent}{type_str}: {Fore.GREEN}{obj.__name__}{Style.RESET_ALL}")

    else:
        print(f"{indent}{type_str}:")

        attributes = {name: value for name, value in inspect.getmembers(obj)
                      if not name.startswith('_') and not callable(value)}

        if attributes:
            for name, value in attributes.items():
                print(f"{indent}  {Style.BRIGHT}{name}{Style.RESET_ALL} →")
                debug_dump(value, max_depth, _depth + 4, _seen)
        else:
            print(f"{indent}  {Fore.YELLOW}[No public attribute]{Style.RESET_ALL}")


def debug_dump_and_die(*args, **kwargs) -> None:
    debug_dump(*args, **kwargs)
    exit()


def dd(*args, **kwargs) -> None:
    debug_dump_and_die(*args, **kwargs)


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
