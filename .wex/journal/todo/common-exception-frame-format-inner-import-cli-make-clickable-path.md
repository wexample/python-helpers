# Inner import of cli_make_clickable_path in format() adds per-call overhead

**Source**: `packages/helpers/src/wexample_helpers/common/exception/frame.py:24`
**Agent**: agent:performance
**Bucket**: benchmark-first
**Severity**: perf

## Symptom
`cli_make_clickable_path` is imported inside `format()` on every call rather than at module level, incurring a `sys.modules` dict lookup each invocation.

## Suggested direction
Audit whether the inner placement avoids a circular import; if not, promote the import to module level. If circular, consider a lazy module-level attribute or a TYPE_CHECKING guard to keep startup clean.
