# _is_typed_dict: early return on __annotations__ + __total__ is too broad

**Source**: `packages/helpers/src/wexample_helpers/helpers/type.py:333`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: inconsistency

## Symptom
The first branch inside `_is_typed_dict` returns `True` for any class that has both `__annotations__` and `__total__`, gated only on `__module__` and `__name__` (which virtually every class has). This fires before the stricter four-attribute fallback check at line 356 that also requires `__required_keys__` and `__optional_keys__`, potentially producing false positives for non-TypedDict classes.

## Suggested direction
Remove or strengthen the early return so that only the four-attribute check (plus metaclass checks) determines the result, eliminating the looser premature shortcut.
