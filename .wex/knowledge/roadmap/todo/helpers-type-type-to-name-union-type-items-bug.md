# type_to_name: uses t.items instead of t.__args__ for UnionType

**Source**: `packages/helpers/src/wexample_helpers/helpers/type.py:239`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: bug

## Symptom
`" | ".join(type_to_name(it) for it in t.items)` accesses `t.items` on a `types.UnionType` (Python 3.10+ `A | B`), but `UnionType` exposes member types via `__args__`, not `.items`. The AttributeError is silently swallowed by the surrounding `except Exception`, causing the function to fall back to `str(t)` instead of the structured join.

## Suggested direction
Replace `t.items` with `t.__args__` so the structured join actually executes for PEP 604 union types.
