import pathlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


def module_load_class_from_file(file_path: pathlib.Path, class_name: str) -> type:
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
    module, base_class: type | None = None, skip_prefixes: list[str] | None = None
) -> dict[str, type]:
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
    collected: dict[str, type] = {}

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


def module_are_same(a: Any, b: Any) -> bool:
    """Determine if two class definition are the same class definition"""
    import hashlib
    import inspect
    import os
    import sys

    if a is b:
        return True

    if not isinstance(a, type) or not isinstance(b, type):
        return False

    def class_signature(
        c: type,
    ) -> tuple[str | None, str | None, int | None, str | None, str | None]:
        mod_name = getattr(c, "__module__", None)
        qualname = getattr(c, "__qualname__", None)

        try:
            src_file = inspect.getsourcefile(c) or inspect.getfile(c)
        except TypeError:
            src_file = None
        if src_file:
            src_file = os.path.realpath(src_file)

        try:
            src_lines, lineno = inspect.getsourcelines(c)
            src_hash = hashlib.sha1("".join(src_lines).encode("utf-8")).hexdigest()
        except (OSError, TypeError):
            lineno = None
            src_hash = None

        mod_file = None
        if mod_name and mod_name in sys.modules:
            mod = sys.modules[mod_name]
            mod_file = getattr(mod, "__file__", None)
            if mod_file:
                mod_file = os.path.realpath(mod_file)

        return (src_file, mod_file, lineno, src_hash, qualname)

    a_sig = class_signature(a)
    b_sig = class_signature(b)

    a_src_file, a_mod_file, a_lineno, a_hash, a_qual = a_sig
    b_src_file, b_mod_file, b_lineno, b_hash, b_qual = b_sig

    if (
        a_src_file
        and b_src_file
        and a_src_file == b_src_file
        and a_qual == b_qual
        and a_hash
        and b_hash
        and a_hash == b_hash
    ):
        return True

    if (
        a_mod_file
        and b_mod_file
        and a_mod_file == b_mod_file
        and a_qual == b_qual
        and a_hash
        and b_hash
        and a_hash == b_hash
    ):
        return True

    if (
        getattr(a, "__module__", None) == getattr(b, "__module__", None)
        and a_qual == b_qual
    ):
        return True

    return False
