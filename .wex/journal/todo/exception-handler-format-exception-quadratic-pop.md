# format_exception: O(n²) list slicing in dunder-trim while loop

**Source**: `packages/helpers/src/wexample_helpers/common/exception/handler.py:63`
**Agent**: agent:performance
**Bucket**: benchmark-first
**Severity**: perf

## Symptom
`while frames and _is_dunder(frames[-1].function): frames = frames[:-1]` creates a new list on every iteration, making the trim O(n²) in the number of trailing dunder frames.

## Suggested direction
Replace with `frames.pop()` (O(1) per iteration) after confirming `TraceCollector.from_traceback` does not retain an external reference to the returned list; alternatively convert to a reverse-scan index and use a single slice at the end.
