from __future__ import annotations

import sys
from pathlib import Path


def system_get_venv_bin_path() -> Path:
    return Path(sys.executable).parent
