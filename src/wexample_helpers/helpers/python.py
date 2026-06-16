from __future__ import annotations

import re

_ARROW_PATTERN = re.compile(r"->\s*['\"]?([\w\d_]+)['\"]?")
_RETURNS_PATTERN = re.compile(r"Returns\s+['\"]?([\w\d_]+)['\"]?")


def python_get_return_type_from_annotations(func) -> str | None:
    annotations = getattr(func, "__annotations__", None)
    if not annotations or "return" not in annotations:
        return None

    return_annotation = annotations["return"]

    if hasattr(return_annotation, "__name__"):
        return return_annotation.__name__
    return str(return_annotation).replace("typing.", "")


def python_get_return_type_from_docstring(docstring: str | None) -> str | None:
    if not docstring:
        return None

    arrow_match = _ARROW_PATTERN.search(docstring)
    if arrow_match:
        return arrow_match.group(1)

    returns_match = _RETURNS_PATTERN.search(docstring)
    if returns_match:
        return returns_match.group(1)

    return None
