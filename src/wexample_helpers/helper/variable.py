from __future__ import annotations

from typing import Any

# Module-level dispatch table: avoids repeated isinstance checks and MRO traversal
# on every call. Uses the faster .copy() C-methods instead of constructors.
_SHALLOW_COPY_DISPATCH: dict[type, Any] = {
    list: list.copy,
    dict: dict.copy,
    set: set.copy,
}


def copy_shallow(x: Any) -> Any:
    fn = _SHALLOW_COPY_DISPATCH.get(type(x))
    if fn is not None:
        return fn(x)
    return x  # immutables (tuple, str, int, …)
