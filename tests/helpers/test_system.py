from __future__ import annotations

import sys
from pathlib import Path


def test_system_get_venv_bin_path_returns_executable_parent() -> None:
    from wexample_helpers.helpers.system import system_get_venv_bin_path

    result = system_get_venv_bin_path()
    assert result == Path(sys.executable).parent
    assert result.exists()
