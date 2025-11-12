from pydantic import BaseModel

from wexample_helpers.common.exception.handler import ExceptionHandler
from wexample_helpers.enums.debug_path_style import DebugPathStyle


def make_boom():
    def inner():
        raise ValueError("boom from example")

    def middle():
        inner()

    middle()


def demo_exception_full_paths():
    print("\n=== Exception with FULL paths ===\n")
    handler = ExceptionHandler()
    try:
        make_boom()
    except Exception as e:
        print(handler.format_exception(e, path_style=DebugPathStyle.FULL))


def demo_exception_filename_only():
    print("\n=== Exception with FILENAME only ===\n")
    handler = ExceptionHandler()
    try:
        make_boom()
    except Exception as e:
        print(handler.format_exception(e, path_style=DebugPathStyle.FILENAME))


def demo_exception_with_paths_map():
    print("\n=== Exception with paths_map substitution ===\n")
    handler = ExceptionHandler()
    # Emulate replacing "/app" prefix by current working directory
    import os
    paths_map = {"/app": os.getcwd()}
    try:
        make_boom()
    except Exception as e:
        print(handler.format_exception(e, path_style=DebugPathStyle.FULL, paths_map=paths_map))


def demo_exception_pydantic_unexpected_property():
    class TestPydanticModel(BaseModel):
        property: bool

    instance = TestPydanticModel(property=True)
    handler = ExceptionHandler()

    try:
        instance.unexpected_property
    except Exception as e:
        print(handler.format_exception(e, path_style=DebugPathStyle.FULL))


if __name__ == "__main__":
    demo_exception_full_paths()
    demo_exception_filename_only()
    demo_exception_with_paths_map()
    demo_exception_pydantic_unexpected_property()
