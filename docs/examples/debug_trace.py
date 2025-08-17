from wexample_helpers.common.debug.debug_trace import DebugTrace
from wexample_helpers.enums.debug_path_style import DebugPathStyle


def demo_trace_default():
    def nested():
        DebugTrace(path_style=DebugPathStyle.FULL).print()
    nested()


def demo_trace_with_internal():
    def nested():
        DebugTrace(path_style=DebugPathStyle.FULL, show_internal=True).print()
    nested()


if __name__ == "__main__":
    print("-- DebugTrace (default, internal hidden) --")
    demo_trace_default()
    print("\n-- DebugTrace (with internal) --")
    demo_trace_with_internal()
