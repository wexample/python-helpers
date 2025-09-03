from wexample_helpers.common.debug.debug_dump import DebugDump
from wexample_helpers.common.debug.debug_dump_class import DebugDumpClass
from wexample_helpers.common.debug.debug_breakpoint import DebugBreakpoint


class Foo:
    class_attr = 42

    def __init__(self):
        self.x = [1, 2, {"a": 3}]
        self._hidden = "secret"

    @property
    def name(self):
        return "foo"


def demo_dump():
    obj = {
        "s": "hello",
        "n": 123,
        "lst": [1, 2, 3],
        "inst": Foo(),
    }
    # Print dump to console
    DebugDump(obj).print()


def demo_dump_class():
    # Show class hierarchy and attributes
    DebugDumpClass(Foo).print()


def demo_breakpoint():
    # Show help and enter pdb. Comment this line if you don't want to stop.
    DebugBreakpoint("Inspect state before proceeding").print()


if __name__ == "__main__":
    print("-- DebugDump --")
    demo_dump()
    print("\n-- DebugDumpClass --")
    demo_dump_class()
    # Uncomment to try the breakpoint demo
    # print("\n-- DebugBreakpoint --")
    # demo_breakpoint()
