# debug_timer_end: precision parameter accepted but never applied

**Source**: `packages/helpers/src/wexample_helpers/helpers/debug.py:44`
**Agent**: agent:performance
**Bucket**: bug
**Severity**: bug

## Symptom
`debug_timer_end(name, precision=2)` accepts a `precision` argument but the return value is a raw float; rounding is never applied, so callers that rely on precision get unrounded results.

## Suggested direction
Either apply `round(..., precision)` to the return value, or remove the parameter from the signature if rounding was never intended.
