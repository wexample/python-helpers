# _collect_data copies `seen` set for every sibling element

**Source**: `packages/helpers/src/wexample_helpers/common/debug/debug_dump.py:55`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: perf

## Symptom
`seen.copy()` is called once per element inside the list/tuple/set and dict comprehensions (lines 55, 63, 64, 95). For a large container with a deep `seen` set already built up, this is O(n × |seen|) copying per container level.

## Suggested direction
Replace set-copy-per-sibling with backtracking (add obj_id before recursion, remove after); this shares a single mutable `seen` across siblings while still detecting cycles on any single root-to-leaf path. Requires verifying that the new behaviour (shared seen across siblings) matches the intended circular-reference policy.
