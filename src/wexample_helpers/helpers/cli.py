from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wexample_helpers.const.types import PathOrString

# Hoisted to module level: frozenset built once, avoids per-call allocation.
_BOOL_TRUTHY: frozenset[str] = frozenset({"true", "yes", "y", "1"})

# Dispatch table replaces a linear elif chain with a single O(1) dict lookup.
_CLI_TYPE_CONVERTERS: dict[type, Any] = {
    bool: lambda v: v.lower() in _BOOL_TRUTHY,
    int: int,
    float: float,
    str: str,
    list: lambda v: [item.strip() for item in v.split(",")],
}


def cli_argument_convert_value(value: str, target_type: type) -> Any:
    """
    Convert an argument value to the target type.
    """
    converter = _CLI_TYPE_CONVERTERS.get(target_type)
    if converter is not None:
        return converter(value)
    # For custom types, try to use the constructor
    return target_type(value)


def cli_make_clickable_path(
    path: PathOrString, short_title: bool | PathOrString = False
) -> str:
    from pathlib import Path

    if short_title is True:
        display_text = Path(path).name
    elif short_title is False:
        display_text = path
    else:
        display_text = str(short_title)

    # \033]8;;file://{path}\033\\  : Link start
    # \033]8;;\033\\              : Link end
    return f"\033]8;;file://{path}\033\\{display_text}\033]8;;\033\\"
