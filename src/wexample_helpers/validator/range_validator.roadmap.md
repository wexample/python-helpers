# RangeValidator — Roadmap

## Correctness: `bool` passes numeric type check

`isinstance(True, (int, float))` returns `True` in Python because `bool` is a
subclass of `int`.  This means `RangeValidator.validate(True)` currently returns
`True` (or `False` only if 0/1 falls outside the configured range), which is
almost certainly unintended for a *numeric range* validator.

**Suggested fix** — reject booleans explicitly before the numeric check:

```python
if isinstance(value, bool) or not isinstance(value, (int, float)):
    return False
```

This keeps the fast-path order and avoids importing extra modules.
