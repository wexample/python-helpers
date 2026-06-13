# directory_aggregate_all_files: redundant Path(fp) wrapping before os.fspath

**Source**: `packages/helpers/src/wexample_helpers/helpers/directory.py:23`
**Agent**: agent:performance
**Bucket**: redundant-check
**Severity**: perf

## Symptom
`os.fspath(Path(fp))` constructs a Path object only to immediately convert it back to a string; `os.fspath(fp)` handles both `str` and `Path` inputs directly, making the intermediate `Path(fp)` allocation unnecessary on every iteration.

## Suggested direction
Replace `os.fspath(Path(fp))` with `os.fspath(fp)` and remove the now-unused `from pathlib import Path` import inside the function; blocked on this pass by the no-import-change rule.
