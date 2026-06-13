# ansi_truncate_visible calls ansi_strip_invisible twice on truncating path

**Source**: `packages/helpers/src/wexample_helpers/helpers/ansi.py:55`
**Agent**: agent:performance
**Bucket**: benchmark-first
**Severity**: perf

## Symptom
`ansi_truncate_visible` calls `ansi_display_width` (which internally calls `ansi_strip_invisible`) at line 55 for the early-return guard, then calls `ansi_strip_invisible` again at line 57 when truncation is actually needed, doubling the stripping work on the common truncating path.

## Suggested direction
Hoist a single `ansi_strip_invisible(text)` call before both uses and thread the `plain` result into a local `ansi_display_width` that accepts pre-stripped input, or restructure the guard to reuse the already-stripped string; profile first on realistic inputs to confirm this is a meaningful hot path.
