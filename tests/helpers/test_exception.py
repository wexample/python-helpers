import os
import sys
import re

# Ensure local helpers are importable
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
HELPERS_PATH = os.path.join(PROJECT_ROOT, "pip", "helpers")
sys.path.insert(0, HELPERS_PATH)

from wexample_helpers.helpers.error import error_format  # type: ignore  # noqa: E402
from wexample_helpers.enums.debug_path_style import DebugPathStyle  # type: ignore  # noqa: E402


def _raise_nested():
    def inner():
        raise ValueError("boom")

    def middle():
        inner()

    middle()


def test_error_format_contains_exception_and_frames():
    try:
        _raise_nested()
    except Exception as e:  # noqa: PIE786
        out = error_format(e, path_style=DebugPathStyle.FULL)

    # Should end with the exception message
    assert out.strip().endswith("ValueError: boom")

    # Should contain at least one formatted frame header
    assert "File     :" in out
    assert "Function :" in out

    # Contains this test function name
    assert "test_error_format_contains_exception_and_frames" in out

    # Contains path with a colon and line number pattern
    assert re.search(r":\d+\nLine\s+:\s+\d+", out) is not None
