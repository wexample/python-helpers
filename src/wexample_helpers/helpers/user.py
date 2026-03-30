from __future__ import annotations

import os


def user_get_real_username() -> str:
    """Return the real username, falling back to SUDO_USER when running under sudo."""
    return os.environ.get("SUDO_USER") or os.environ.get("USER") or os.getlogin()
