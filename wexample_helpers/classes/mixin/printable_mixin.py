class PrintableMixin:
    def __str__(self):
        from wexample_helpers.debug.debug_dump_class import DebugDumpClass
        return DebugDumpClass(self).print(silent=True)
