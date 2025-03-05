import inspect
from typing import Any
from typing import Optional, TYPE_CHECKING

from wexample_helpers.enums.debug_path_style import DebugPathStyle
from wexample_helpers.helpers.trace import trace_print

if TYPE_CHECKING:
    pass

# ANSI color codes
class Colors:
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RESET = '\033[0m'
    BRIGHT = '\033[1m'

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


def _format_class_hierarchy(cls, depth=0, seen=None):
    if seen is None:
        seen = set()
    
    if cls in seen:
        return [f"{' ' * depth}{Colors.YELLOW}↻ {cls.__name__} (circular){Colors.RESET}"]
    seen.add(cls)
    
    result = []
    class_info = f"{' ' * depth}{Colors.BLUE}→ {cls.__name__}{Colors.RESET}"
    
    # Add module info
    if cls.__module__ != "__main__":
        class_info += f" {Colors.GREEN}({cls.__module__}){Colors.RESET}"
    
    result.append(class_info)
    
    # Add attributes
    attrs = {name: value for name, value in cls.__dict__.items() 
            if not name.startswith('__') and not callable(value)}
    if attrs:
        for name, value in attrs.items():
            result.append(f"{' ' * (depth + 2)}{Colors.BRIGHT}{name}{Colors.RESET}: {Colors.GREEN}{repr(value)}{Colors.RESET}")
    
    # Recursively process base classes
    for base in cls.__bases__:
        if base is not object:  # Skip the base object class
            result.extend(_format_class_hierarchy(base, depth + 4, seen.copy()))
    
    return result

def debug_class_info(cls_or_obj, title: str = None) -> None:
    """
    Print detailed information about a class or object with improved hierarchy visualization.
    """
    target_class = cls_or_obj if isinstance(cls_or_obj, type) else type(cls_or_obj)

    if title:
        print(f"\n{Colors.BRIGHT}=== {title} ==={Colors.RESET}")

    for line in _format_class_hierarchy(target_class):
        print(line)

def debug_dump(obj: Any, max_depth: int = 100, _depth: int = 0, _seen=None) -> None:
    if _seen is None:
        _seen = set()

    if _depth > max_depth:
        print(f"{' ' * _depth}{Colors.YELLOW}[Max depth reached]{Colors.RESET}")
        return

    obj_id = id(obj)
    if obj_id in _seen and not isinstance(obj, (int, float, str, bool)):
        print(f"{' ' * _depth}{Colors.YELLOW}[Circular reference]{Colors.RESET}")
        return
    _seen.add(obj_id)

    indent = ' ' * _depth
    
    # If it's a class, use debug_class_info
    if inspect.isclass(obj):
        for line in _format_class_hierarchy(obj, _depth):
            print(line)
        return
    
    # For custom class instance
    if hasattr(obj, '__class__') and not isinstance(obj, (int, float, str, bool, list, tuple, dict)):
        print(f"{indent}{Colors.BLUE}Instance of {obj.__class__.__name__}{Colors.RESET}")
        for line in _format_class_hierarchy(obj.__class__, _depth + 2):
            print(line)
        
        # Display instance attributes
        instance_attrs = {name: value for name, value in inspect.getmembers(obj)
                        if not name.startswith('_') and not callable(value)}
        if instance_attrs:
            print(f"{indent}{Colors.BRIGHT}Instance attributes:{Colors.RESET}")
            for name, value in instance_attrs.items():
                print(f"{indent}  {Colors.BRIGHT}{name}{Colors.RESET} →")
                debug_dump(value, max_depth, _depth + 4, _seen)
        return

    obj_type = type(obj).__name__
    type_str = f"{Colors.BLUE}{obj_type}{Colors.RESET}"

    if obj is None:
        print(f"{indent}{type_str}: {Colors.BRIGHT}None{Colors.RESET}")

    elif isinstance(obj, (int, float, str, bool)):
        print(f"{indent}{type_str}: {Colors.GREEN}{repr(obj)}{Colors.RESET}")

    elif isinstance(obj, (list, tuple)):
        print(f"{indent}{type_str} ({len(obj)} elements):")
        for i, item in enumerate(obj):
            print(f"{indent}  {Colors.BRIGHT}[{i}]{Colors.RESET} →")
            debug_dump(item, max_depth, _depth + 4, _seen)

    elif isinstance(obj, dict):
        print(f"{indent}{type_str} ({len(obj)} elements):")
        for key, value in obj.items():
            print(f"{indent}  {Colors.BRIGHT}{repr(key)}{Colors.RESET} →")
            debug_dump(value, max_depth, _depth + 4, _seen)

    elif inspect.isfunction(obj) or inspect.ismethod(obj):
        print(f"{indent}{type_str}: {Colors.GREEN}{obj.__name__}{Colors.RESET}")

    else:
        print(f"{indent}{type_str}:")

        attributes = {name: value for name, value in inspect.getmembers(obj)
                      if not name.startswith('_') and not callable(value)}

        if attributes:
            for name, value in attributes.items():
                print(f"{indent}  {Colors.BRIGHT}{name}{Colors.RESET} →")
                debug_dump(value, max_depth, _depth + 4, _seen)
        else:
            print(f"{indent}  {Colors.YELLOW}[No public attribute]{Colors.RESET}")


def debug_dump_and_die(*args, **kwargs) -> None:
    debug_dump(*args, **kwargs)
    exit()


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


def dd(*args, **kwargs) -> None:
    debug_dump_and_die(*args, **kwargs)