# Resserrer `BaseClass._validate_field_types` (sans tout casser)

**Source**: `packages/helpers/src/wexample_helpers/classes/base_class.py`
**Severity**: tech-debt (latent correctness)

## Symptom

Le validator a actuellement un dead-code path qui **silencieusement tolère**
les déclarations de champs nues sur des descendants de `BaseClass`:

```python
@base_class
class Foo(BaseClass):
    value: int = 42           # ← devrait raise, passe en silence
    is_setup: bool = False    # ← devrait raise, passe en silence
```

Une tentative de "nettoyage du dead elif" (perf commit `5d39d0c`, revert par
`c83bc1c` le 2026-06-15) a fait fire le validator comme prévu… mais a
révélé **118 violations latentes** à travers les packages, dont une
poignée bloquent l'import de `wex` complètement. Trop volumineux pour fixer
à chaud, le revert a restauré le statu quo permissif.

## Scan d'inventaire

Script AST pour lister les violations:

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

Au 2026-06-15: **118 violations**, dont:

- **~13 caches du perf agent** (`_options_cache`, `_allowed_options_cache`,
  `_raw_value_type_cache`) — pas des vraies violations, des MRO leaks à
  **revert** séparément (voir ticket distinct sur les caches perf).
- **~10 `error_code: str = "..."`** sur des exceptions —
  devraient être `ClassVar[str]` (constantes de classe, pas instance
  fields).
- **~70 instance fields** sur des classes pseudocode / configs / testing —
  à wrapper avec `public_field`/`private_field`.
- **~20 candidats false positives** (classes qui n'héritent pas
  effectivement de `BaseClass` mais matchent au grep AST naïf).

## Suggested direction

Trois étapes, à faire dans cet ordre:

1. **Affiner le scanner** pour ne lister que les classes effectivement
   descendantes de `BaseClass` (construire le graphe d'héritage transitif
   via AST, ou via import et `mro()` sur un environnement de test). Élimine
   les false positives, donne le vrai périmètre.
2. **Catégoriser et corriger** chaque vraie violation:
   - `error_code` et autres constantes → `ClassVar[type] = value`
   - Caches perf → revert le commit perf concerné
   - Instance fields → wrapper `public_field` / `private_field`
3. **Réappliquer** le revert de `c83bc1c` (qui rétablit le validator
   strict). Soit via un cherry-pick, soit en faisant le `revert du revert`,
   soit en réécrivant proprement la branche `_validate_field_types`.

À étudier: faut-il assouplir le validator pour les classes mixin pures
(non `@base_class`) qui se retrouvent dans le MRO d'un `BaseClass`? Le
fix `abstract_local_item_path.py` (`98fd117`) suggère que ces cas
existent et que la règle "tout champ doit être un BaseField" est trop
restrictive pour eux.

## État actuel

- Validator: **permissif** (5d39d0c reverted via c83bc1c)
- Fix follow-ups gardés: `dd7b91f`, `328e2cf`, `98fd117` — ils sont
  toujours corrects (le wrapper est valide même avec validator permissif),
  juste plus *obligatoires*.
- Bug structurel `get_allowed_options_registry` (commit `fc6e8a0`):
  **fixé en place** dans `wexample_config`, n'est pas concerné par ce
  ticket.
