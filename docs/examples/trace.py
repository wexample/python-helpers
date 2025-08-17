from wexample_helpers.helpers.trace import trace_print
from wexample_helpers.enums.debug_path_style import DebugPathStyle


def demo_trace():
    def nested():
        # Default: internal helper frame hidden
        trace_print(path_style=DebugPathStyle.FULL)

    nested()


def demo_trace_with_internal():
    def nested():
        # Explicitly show internal helper frame
        trace_print(path_style=DebugPathStyle.FULL, show_internal=True)

    nested()


if __name__ == "__main__":
    demo_trace()
    print("\n-- with internal helper frame --\n")
    demo_trace_with_internal()
