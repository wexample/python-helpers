# Resserrer `BaseClass._validate_field_types` (sans tout casser)

**Source**: `packages/helpers/src/wexample_helpers/classes/base_class.py`
**Severity**: tech-debt (latent correctness)

## Symptom

The validator currently has a dead-code path that **silently tolerates**
bare field declarations on descendants of `BaseClass`:

```python
@base_class
class Foo(BaseClass):
    value: int = 42           # ← devrait raise, passe en silence
    is_setup: bool = False    # ← devrait raise, passe en silence
```

An attempt to "clean up the dead elif" (perf commit `5d39d0c`, reverted by
`c83bc1c` on 2026-06-15) fired the validator as expected… but revealed
**118 latent violations** across packages, a handful of which block the
import of `wex` entirely. Too large to fix on the spot, the revert restored
the permissive status quo.

## Inventory scan

AST script to list the violations:

```python
import ast
from pathlib import Path

ROOTS = [
    Path("packages/PYTHON/packages"),
    Path("packages/PYTHON/wex"),
]
FIELD_CALLS = {"public_field", "private_field", "protected_field", "Factory", "field"}

def is_field_call(value):
    if isinstance(value, ast.Call):
        func = value.func
        name = func.id if isinstance(func, ast.Name) else (func.attr if isinstance(func, ast.Attribute) else None)
        return name in FIELD_CALLS
    return False

def is_classvar(ann):
    if isinstance(ann, ast.Subscript):
        v = ann.value
        if isinstance(v, ast.Name) and v.id == "ClassVar":
            return True
        if isinstance(v, ast.Attribute) and v.attr == "ClassVar":
            return True
    if isinstance(ann, ast.Name) and ann.id == "ClassVar":
        return True
    return False

def scan(path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, SyntaxError):
        return []
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for stmt in node.body:
            if not isinstance(stmt, ast.AnnAssign) or stmt.value is None:
                continue
            if not isinstance(stmt.target, ast.Name):
                continue
            if is_classvar(stmt.annotation) or is_field_call(stmt.value):
                continue
            if stmt.target.id.isupper():
                continue
            out.append((stmt.lineno, node.name, stmt.target.id))
    return out
```

As of 2026-06-15: **118 violations**, including:

- **~13 perf-agent caches** (`_options_cache`, `_allowed_options_cache`,
  `_raw_value_type_cache`) — not real violations, MRO leaks to
  **revert** separately (see the separate ticket on perf caches).
- **~10 `error_code: str = "..."`** on exceptions —
  should be `ClassVar[str]` (class constants, not instance fields).
- **~70 instance fields** on pseudocode / config / testing classes —
  to be wrapped with `public_field`/`private_field`.
- **~20 false-positive candidates** (classes that do not actually inherit
  from `BaseClass` but match the naive AST grep).

## Suggested direction

Three steps, in this order:

1. **Refine the scanner** to list only classes that are genuine descendants
   of `BaseClass` (build the transitive inheritance graph via AST, or via
   import and `mro()` in a test environment). Eliminates false positives,
   gives the true scope.
2. **Categorise and fix** each real violation:
   - `error_code` and other constants → `ClassVar[type] = value`
   - Perf caches → revert the relevant perf commit
   - Instance fields → wrap with `public_field` / `private_field`
3. **Re-apply** the revert of `c83bc1c` (which restores the strict
   validator). Either via cherry-pick, via a revert-of-the-revert, or by
   cleanly rewriting the `_validate_field_types` branch.

To investigate: should the validator be relaxed for pure mixin classes
(non `@base_class`) that end up in the MRO of a `BaseClass`? The fix in
`abstract_local_item_path.py` (`98fd117`) suggests these cases exist and
that the rule "every field must be a BaseField" is too restrictive for them.

## Current state

- Validator: **permissive** (5d39d0c reverted via c83bc1c)
- Follow-up fixes kept: `dd7b91f`, `328e2cf`, `98fd117` — they are
  still correct (the wrapper is valid even with a permissive validator),
  just no longer *mandatory*.
- Structural bug `get_allowed_options_registry` (commit `fc6e8a0`):
  **fixed in place** in `wexample_config`, not in scope for this ticket.
