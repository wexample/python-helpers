# string_convert_case_map rebuilds dict on every call

**Source**: `packages/helpers/src/wexample_helpers/helpers/string.py:48`
**Agent**: agent:performance
**Bucket**: benchmark-first
**Severity**: perf

## Symptom
`string_convert_case` calls `string_convert_case_map()` on every invocation; that function allocates and returns a new dict of 8 entries each time with no caching.

## Suggested direction
Add `@lru_cache(maxsize=1)` (already imported) to `string_convert_case_map`; the dict is constant so the cached copy is always valid.
