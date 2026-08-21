# Registry raises spurious KeyError when stored value is None

**Source**: `packages/helpers/src/wexample_helpers/service/registry.py:81`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: bug

## Symptom
`_raise_error_if_expected` checks `item is None` to detect a missing entry, but
`dict.get(key)` returns `None` both for absent keys and for keys whose value was
explicitly registered as `None`. A caller that stores `None` and later calls `get()`
with `_fail_if_missing=True` receives a spurious `KeyError`.

## Suggested direction
Replace the sentinel check with `key not in self._items` so absence is detected
independently of the stored value.
