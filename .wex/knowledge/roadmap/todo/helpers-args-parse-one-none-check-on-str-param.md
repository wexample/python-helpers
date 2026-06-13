# args_parse_one: None guard on a str-typed parameter

**Source**: `packages/helpers/src/wexample_helpers/helpers/args.py:81`
**Agent**: agent:performance
**Bucket**: redundant-check
**Severity**: typing

## Symptom
`args_parse_one` is typed `argument: str` but its first guard is `if argument is None or argument == ""`. The `None` branch is either dead code (if callers always pass a str) or the type annotation is incorrect (if None can arrive at runtime).

## Suggested direction
Audit call sites to confirm whether `None` is ever passed; if not, drop the `is None` guard and tighten the annotation to remove ambiguity.
