# dict_merge benchmark tests share mutable inputs across repeated iterations

**Source**: `benchmarks/test_benchmark.py:225`
**Agent**: agent:performance
**Bucket**: bug
**Severity**: bug

## Symptom
`test_dict_merge_two_shallow`, `test_dict_merge_three_dicts`, and `test_dict_merge_nested`
pass the same dict objects (`_DICT_A`, `_DICT_B`, `_DICT_C`, `a`, `b`) directly to
`benchmark(dict_merge, ...)`. The framework calls `dict_merge(...)` N times on the
identical references. If `dict_merge` mutates any of its arguments the second and
subsequent calls operate on already-merged state, making timing results meaningless and
potentially hiding errors.

## Suggested direction
Wrap each benchmark in a `_merge()` inner callable that builds fresh copies of the
input dicts on every invocation (e.g. `copy.deepcopy` or explicit dict literals), then
pass the callable to `benchmark(_merge)`.
