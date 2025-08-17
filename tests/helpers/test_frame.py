import os
import sys

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
HELPERS_PATH = os.path.join(PROJECT_ROOT, "pip", "helpers")
sys.path.insert(0, HELPERS_PATH)

from wexample_helpers.common.exception.frame import ExceptionFrame  # type: ignore  # noqa: E402
from wexample_helpers.enums.debug_path_style import DebugPathStyle  # type: ignore  # noqa: E402


def test_exception_frame_formatting_full_and_filename(tmp_path):
    # Create a temp file to simulate a real path
    p = tmp_path / "module" / "file.py"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("print('x')\n")

    frame = ExceptionFrame(
        filename=str(p),
        lineno=1,
        function="foo",
        code="print('x')\n",
        path_style=DebugPathStyle.FULL,
    )

    rendered = str(frame)
    assert "File     :" in rendered
    assert "Function : foo" in rendered
    assert str(p) in rendered

    # Basename/FILENAME style
    frame2 = ExceptionFrame(
        filename=str(p),
        lineno=1,
        function="bar",
        code=None,
        path_style=DebugPathStyle.FILENAME,
    )
    rendered2 = str(frame2)
    assert os.path.basename(str(p)) + ":1" in rendered2


def test_exception_frame_paths_map_substitution(tmp_path):
    prod = "/var/app"
    local = str(tmp_path)
    target = os.path.join(prod, "src", "x.py")
    frame = ExceptionFrame(
        filename=target,
        lineno=10,
        function="baz",
        code=None,
        path_style=DebugPathStyle.FULL,
        paths_map={prod: local},
    )
    rendered = str(frame)
    # The path shown should be replaced to local
    assert local in rendered
