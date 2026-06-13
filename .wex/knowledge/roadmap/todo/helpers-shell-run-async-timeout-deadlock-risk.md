# shell_run_async timeout path: potential deadlock when capturing output

**Source**: `packages/helpers/src/wexample_helpers/helpers/shell.py:225`
**Agent**: agent:performance
**Bucket**: benchmark-first
**Severity**: bug

## Symptom
In the `timeout is not None` branch, `asyncio.wait_for(proc.wait(), timeout)` is called to wait for process completion, then `proc.communicate()` is called afterward to read stdout/stderr. If the process produces enough output to fill the OS pipe buffer, `proc.wait()` will never complete (the process blocks writing to the pipe while nothing is consuming it), causing a deadlock.

## Suggested direction
Replace `wait_for(proc.wait(), timeout)` followed by `communicate()` with a single `wait_for(proc.communicate(), timeout)` call, which drains the pipes and waits concurrently — the established asyncio-safe pattern.
