import pathlib
from typing import Optional, Type, List, Dict

from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def module_load_class_from_file(file_path: pathlib.Path, class_name: str) -> Type:
    import importlib

    """Load a class by name from a python module file path."""
    if not file_path.exists():
        raise FileNotFoundError(f"Module file not found: {file_path}")

    module_name = f"wex_dynamic_{abs(hash(str(file_path)))}"
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot create a spec for module: {file_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]

    try:
        cls = getattr(module, class_name)
    except AttributeError as e:
        raise ImportError(
            f"Class '{class_name}' not found in module '{file_path}'."
        ) from e

    return cls


def module_collect_classes(
        module,
        base_class: Optional[Type] = None,
        skip_prefixes: Optional[List[str]] = None
) -> Dict[str, Type]:
    import inspect

    """
    Collects non-abstract classes from a module, optionally filtering by base class and prefix.

    Args:
        module: The module to inspect.
        base_class: Optional base class to filter by.
        skip_prefixes: List of prefixes for class names to skip (e.g., ['Abstract']).

    Returns:
        Dictionary of class name to class object.
    """
    module_name = module.__name__
    collected: Dict[str, Type] = {}

    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ != module_name:
            continue
        if inspect.isabstract(obj):
            continue
        if skip_prefixes and any(name.startswith(p) for p in skip_prefixes):
            continue
        if base_class and not issubclass(obj, base_class):
            continue
        collected[name] = obj

    return collected
