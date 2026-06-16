# Deferred items — helpers/helpers/type.py

## 1. `type_to_name`: `t.items` should be `t.__args__`

`types.UnionType` (Python ≥ 3.10 `A | B` syntax) exposes its members via
`__args__`, **not** `.items`.  The current code silently falls back to
`str(t)` via the bare `except Exception`, hiding the bug at runtime.

```python
# current (broken for Python ≥ 3.10 union syntax)
return " | ".join(type_to_name(it) for it in t.items)

# fix
return " | ".join(type_to_name(it) for it in t.__args__)
```

Risk: low — only affects the name-formatting helper.

---

## 2. `_is_typed_dict`: cache `_TypedDictMeta` at module level

The function runs up to **two `import` statements** on every call to detect
`typing_extensions._TypedDictMeta` and `typing._TypedDictMeta`.  Python's
import machinery caches module objects in `sys.modules`, so the extra cost is
a dict look-up + attribute access each time — but it is still avoidable.

Suggested approach: resolve both meta-classes once at module import time and
store the results in module-level variables, then use those in `_is_typed_dict`.

```python
# top of module
try:
    from typing_extensions import _TypedDictMeta as _TE_TypedDictMeta
except ImportError:
    _TE_TypedDictMeta = None  # type: ignore[assignment]

try:
    import typing as _typing
    _T_TypedDictMeta = getattr(_typing, "_TypedDictMeta", None)
except ImportError:
    _T_TypedDictMeta = None
```

Then inside `_is_typed_dict`:
```python
if _TE_TypedDictMeta is not None and isinstance(type_hint, _TE_TypedDictMeta):
    return True
if _T_TypedDictMeta is not None and isinstance(type_hint, _T_TypedDictMeta):
    return True
```

Risk: low, but `_TypedDictMeta` is a private API — pin to tested library
versions before landing.
