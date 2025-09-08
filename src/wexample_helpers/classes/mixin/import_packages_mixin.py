from __future__ import annotations

import importlib
import pkgutil
import sys
from typing import ClassVar


class ImportPackagesMixin:
    """Mixin that accumulates `import_packages` and provides a bootstrap loader.

    - Classes may declare `import_packages` as an iterable of package names.
    - __init_subclass__ merges declarations across the hierarchy (L→R, then self).
    - load_imports() imports modules, builds a parent namespace, and rebuilds Pydantic models.
    """

    import_packages: ClassVar[tuple[str, ...]] = ()
    # Track which concrete classes have completed load_imports()
    _imports_loaded_classes: ClassVar[set[type]] = set()

    @classmethod
    def load_imports(cls) -> None:
        """Import packages from `cls.import_packages` and rebuild Pydantic models.

        This mitigates Pydantic v2 'class-not-fully-defined' errors by ensuring all
        referenced modules are imported before model_rebuild is invoked.
        """
        # Per-class guard using a shared registry (avoid inheritance bleed)
        if cls in ImportPackagesMixin._imports_loaded_classes:
            return

        # Merge packages dynamically from the full MRO (base -> cls)
        merged: list[str] = []
        for c in reversed(cls.mro()):
            merged += list(getattr(c, "import_packages", ()))
        loaded_packages = tuple(dict.fromkeys(merged))

        # Import packages (best effort) and their submodules
        for pkg_name in loaded_packages:
            try:
                pkg = importlib.import_module(pkg_name)
            except Exception:
                continue
            if hasattr(pkg, "__path__"):
                for mod in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
                    try:
                        importlib.import_module(mod.name)
                    except Exception:
                        pass

        # Build a parent namespace composed of symbols from loaded packages
        parent_ns: dict[str, object] = {}
        for name, module in list(sys.modules.items()):
            if not module:
                continue
            if any(
                name == pkg or name.startswith(pkg + ".") for pkg in loaded_packages
            ):
                try:
                    parent_ns.update(vars(module))
                except Exception:
                    pass

        # Rebuild the current class using the populated namespace
        setattr(cls, "__pydantic_parent_namespace__", parent_ns)
        cls.model_rebuild()

        # Mark as loaded for this exact class
        ImportPackagesMixin._imports_loaded_classes.add(cls)
