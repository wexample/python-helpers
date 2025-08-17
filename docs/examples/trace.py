from wexample_helpers.helpers.trace import trace_print
from wexample_helpers.enums.debug_path_style import DebugPathStyle


def demo_trace():
    def nested():
        trace_print(path_style=DebugPathStyle.FULL, truncate_stack=1)

    nested()


if __name__ == "__main__":
    demo_trace()
