from __future__ import annotations

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

# Cached after first import to avoid repeated sys.modules + getattr overhead on
# every __str__ call while still deferring the import to prevent circular deps.
_DebugDumpClass = None


@base_class
class PrintableMixin(BaseClass):
    def __str__(self):
        global _DebugDumpClass
        if _DebugDumpClass is None:
            from wexample_helpers.common.debug.debug_dump_class import DebugDumpClass
            _DebugDumpClass = DebugDumpClass
        return _DebugDumpClass(self).print(silent=True)
