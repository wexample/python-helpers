from pathlib import Path


def system_get_venv_bin_path() -> Path:
    import sys

    return Path(sys.executable).parent
