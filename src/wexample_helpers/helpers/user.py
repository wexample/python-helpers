from __future__ import annotations

import os


def user_get_real_gid() -> int:
    """Return the real user's gid, using SUDO_GID when running under sudo."""
    sudo_gid = os.environ.get("SUDO_GID")
    return int(sudo_gid) if sudo_gid else os.getgid()


def user_get_real_uid() -> int:
    """Return the real user's uid, using SUDO_UID when running under sudo."""
    sudo_uid = os.environ.get("SUDO_UID")
    return int(sudo_uid) if sudo_uid else os.getuid()


def user_get_real_username() -> str:
    """Return the real username, falling back to SUDO_USER when running under sudo."""
    return os.environ.get("SUDO_USER") or os.environ.get("USER") or os.getlogin()
