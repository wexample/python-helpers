# string_random_token rebuilds alphabet string on every call

**Source**: `packages/helpers/src/wexample_helpers/helpers/string.py:195`
**Agent**: agent:performance
**Bucket**: hoist
**Severity**: perf

## Symptom
`alphabet = string.ascii_letters + string.digits` concatenates two strings and allocates a new 62-char string on every invocation of `string_random_token`.

## Suggested direction
Hoist `_RANDOM_TOKEN_ALPHABET = string.ascii_letters + string.digits` to module level so the concatenation happens once at import time.
