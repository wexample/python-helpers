# args_shift_one: isinstance(arg, str) on elements of list[str]

**Source**: `packages/helpers/src/wexample_helpers/helpers/args.py:123`
**Agent**: agent:performance
**Bucket**: redundant-check
**Severity**: perf

## Symptom
The loop over `arg_list: list[str]` guards each element with `isinstance(arg, str)` before the regex match. By the type contract every element is already a str; the check is dead on well-typed call paths and adds a per-iteration overhead.

## Suggested direction
Remove the isinstance guard after confirming no call site passes a heterogeneous list; the regex match will raise a TypeError naturally on bad input, which is the correct failure mode.
