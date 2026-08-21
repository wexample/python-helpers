# Duplicate type aliases: PathOrString and FileStringOrPath

**Source**: `packages/helpers/src/wexample_helpers/const/types.py:27,36`
**Agent**: agent:performance
**Bucket**: restructure
**Severity**: inconsistency

## Symptom
`PathOrString = Union[Path, str]` (line 27) and `FileStringOrPath = Union[str, Path]` (line 36) are semantically identical aliases with different names, causing consumer code to use either interchangeably without a canonical choice.

## Suggested direction
Consolidate to a single alias (likely `PathOrString`, the first-defined) and deprecate or remove the duplicate; update all call sites across the suite.
