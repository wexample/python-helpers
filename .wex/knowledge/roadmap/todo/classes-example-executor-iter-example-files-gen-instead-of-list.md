# _iter_example_files could return a generator instead of a list

**Source**: `packages/helpers/src/wexample_helpers/classes/example/executor.py:91`
**Agent**: agent:performance
**Bucket**: gen-instead-of-list
**Severity**: perf

## Symptom
`_iter_example_files` builds and returns a full `list[Path]` even though its only known caller iterates over the result exactly once in a `for` loop.

## Suggested direction
Change the return type to `Iterator[Path]` (or `Generator[Path, None, None]`) and yield paths directly. Verify no other caller relies on list-specific behaviour (indexing, `len`, multiple iterations) before applying.
