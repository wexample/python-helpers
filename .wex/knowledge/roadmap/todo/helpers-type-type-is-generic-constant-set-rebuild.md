# type_is_generic: constant set rebuilt on every call

**Source**: `packages/helpers/src/wexample_helpers/helpers/type.py:211`
**Agent**: agent:performance
**Bucket**: hoist
**Severity**: perf

## Symptom
`generic_types = {list, dict, tuple, Union}` is constructed inside `type_is_generic` on every invocation, allocating a new set object each time. The set is constant and never mutated.

## Suggested direction
Move the set to module level as a private constant (e.g. `_GENERIC_TYPES`) so it is allocated once at import time and reused across all calls.
