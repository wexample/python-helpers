# Redundant inner import of DebugPathStyle in get_formatted_path

**Source**: `packages/helpers/src/wexample_helpers/common/exception/frame.py:42`
**Agent**: agent:performance
**Bucket**: benchmark-first
**Severity**: perf

## Symptom
`DebugPathStyle` is already imported at module level (line 6) but re-imported inside `get_formatted_path()` on every call, adding a `sys.modules` lookup overhead each invocation.

## Suggested direction
Remove the inner import at line 42; the module-level import at line 6 already makes `DebugPathStyle` available. Verify no circular-import issue prevents moving this (likely safe since it is already at module level).
