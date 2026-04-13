from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_helpers.const.types import FileStringOrPath, PathOrString


def file_change_mode(path: PathOrString, mode: int) -> None:
    """
    Change file permissions for a path, ignoring symlinks and missing files.
    """
    try:
        if not os.path.islink(str(path)):
            os.chmod(str(path), mode)
    except FileNotFoundError:
        pass


def file_change_mode_recursive(
    path: PathOrString, mode: int, follow_symlinks: bool = True
) -> None:
    """
    Recursively change mode for files and directories under path.

    :param path: Root path to change mode.
    :param mode: Permission bits to apply.
    :param follow_symlinks: If False, skip symlinked directories.
    """
    file_change_mode(path, mode)
    if os.path.isdir(str(path)) and (follow_symlinks or not os.path.islink(str(path))):
        for item in os.listdir(str(path)):
            file_change_mode_recursive(
                os.path.join(str(path), item), mode, follow_symlinks
            )


def file_chown_recursive(path: PathOrString, uid: int, gid: int) -> None:
    """Recursively set owner uid/gid on a path and all its entries."""
    from pathlib import Path

    p = Path(path)
    os.chown(p, uid, gid)
    for entry in p.rglob("*"):
        try:
            os.chown(entry, uid, gid)
        except OSError:
            pass


def file_get_dir_size(path: PathOrString) -> int:
    """Return total byte size of all files under a directory, skipping unreadable entries."""
    from pathlib import Path

    total = 0
    try:
        for entry in Path(path).rglob("*"):
            try:
                if entry.is_file() and not entry.is_symlink():
                    total += entry.stat().st_size
            except OSError:
                pass
    except OSError:
        pass
    return total


def file_get_directories(path: PathOrString, recursive: bool = False) -> list[str]:
    """Get directories under path, optionally recursively."""
    from pathlib import Path

    base = Path(path)
    if not recursive:
        return [str(p) for p in base.iterdir() if p.is_dir()]
    return [str(p) for p in base.rglob("*") if p.is_dir()]


def file_get_human_readable_size(size: int) -> str:
    """Convert a byte count to a human-readable string (e.g. '1.4 GB')."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def file_list_subdirectories(path: PathOrString) -> list[str]:
    """
    List immediate subdirectory names (excluding hidden) under a given path.
    """
    from pathlib import Path

    base = Path(path)
    subdirs = [
        p.name for p in base.iterdir() if p.is_dir() and not p.name.startswith(".")
    ]
    return sorted(subdirs)


def file_mode_num_to_octal(num: int) -> str:
    """Convert numeric mode (e.g. st_mode) to a three-digit octal string."""
    return oct(num & 0o777)[-3:]


def file_mode_octal_to_num(mode: str | int) -> int:
    """Convert octal mode string (e.g. '755') to its numeric value."""
    return int(str(mode), 8)


def file_path_get_mode_num(path: Path) -> int:
    """Get the numeric permission bits for a Path object."""
    return path.stat().st_mode & 0o777


def file_path_get_octal_mode(path: Path) -> str:
    """Get the octal permission string for a Path object."""
    return file_mode_num_to_octal(path.stat().st_mode)


def file_read(file_path: PathOrString) -> str:
    """Read file content as UTF-8 text."""
    from pathlib import Path

    return Path(file_path).read_text(encoding="utf-8")


def file_read_or_default(
    file_path: PathOrString, default: str | None = ""
) -> str | None:
    """Read file content or return default on any error."""
    try:
        return file_read(file_path)
    except Exception:
        return default


def file_remove_if_exists(path: PathOrString) -> None:
    """Remove a file or symlink if it exists."""
    from pathlib import Path

    p = Path(path)
    if p.is_file() or p.is_symlink():
        p.unlink()


def file_resolve_path(path: FileStringOrPath) -> Path:
    """Resolve a FileStringOrPath to a pathlib.Path object."""
    from pathlib import Path

    return path if isinstance(path, Path) else Path(path)


def file_touch(path: PathOrString, times: tuple[int, int] | None = None) -> None:
    """Create file if missing and update its access and modification times."""
    from pathlib import Path

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a"):
        os.utime(p, times)


def file_mode_is_notation(mode: str) -> bool:
    """Check if mode is a chmod-style notation like +x, -x, +r, -w, etc."""
    return isinstance(mode, str) and len(mode) == 2 and mode[0] in ("+", "-") and mode[1] in "rwx"


def file_mode_apply_notation(current_mode: int, notation: str) -> int:
    """Apply a chmod-style notation (+x, -x, +r, etc.) to a current numeric mode."""
    op = notation[0]
    bit_map = {"r": 0o444, "w": 0o222, "x": 0o111}
    bits = bit_map[notation[1]]
    return current_mode | bits if op == "+" else current_mode & ~bits


def file_validate_mode_octal(mode: str | int) -> bool:
    """Validate that mode is a three-digit octal string or int."""
    m = str(mode)
    return len(m) == 3 and all(ch in "01234567" for ch in m)


def file_validate_mode_octal_or_fail(mode: str | int) -> bool:
    """Validate octal mode or raise Exception."""
    if not file_validate_mode_octal(mode):
        raise ValueError(f"Bad mode format {mode!r}")
    return True


def file_write(file_path: PathOrString, content: str, encoding: str = "utf-8") -> None:
    """Write content to file, overwriting if it exists."""
    from pathlib import Path

    p = Path(file_path)
    p.write_text(content, encoding=encoding)


def file_chown_as_real_user(path: PathOrString) -> None:
    """Chown a path to the real user (handles sudo context)."""
    from wexample_helpers.helpers.user import user_get_real_gid, user_get_real_uid

    os.chown(path, user_get_real_uid(), user_get_real_gid())


def file_chown_as_real_user_if_sudo(path: PathOrString) -> None:
    """Chown a path to the real user only when running under sudo. No-op otherwise."""
    if os.environ.get("SUDO_UID"):
        file_chown_as_real_user(path)


def file_env_append_as_real_user(env_file: PathOrString, env_vars: dict[str, str]) -> None:
    """Append missing KEY=VALUE pairs to an .env file and chown it to the real user."""
    from pathlib import Path

    p = Path(env_file)
    existing = p.read_text() if p.exists() else ""
    new_lines = [f"{k}={v}" for k, v in env_vars.items() if f"{k}=" not in existing]
    if new_lines:
        p.write_text(existing.rstrip("\n") + "\n" + "\n".join(new_lines) + "\n")
        file_chown_as_real_user(p)


def file_copytree_as_real_user(src: PathOrString, dst: PathOrString) -> None:
    """Copy a directory tree to dst and chown all entries to the real user (handles sudo context)."""
    import shutil
    from pathlib import Path

    from wexample_helpers.helpers.user import user_get_real_gid, user_get_real_uid

    uid, gid = user_get_real_uid(), user_get_real_gid()

    def _copy_with_owner(s, d, *, follow_symlinks=True):
        shutil.copy2(s, d, follow_symlinks=follow_symlinks)
        os.chown(d, uid, gid)

    shutil.copytree(src, dst, dirs_exist_ok=True, copy_function=_copy_with_owner)
    for p in Path(dst).rglob("*"):
        os.chown(p, uid, gid)


def file_write_as_real_user(
    file_path: PathOrString, content: str, mode: int = 0o644, encoding: str = "utf-8"
) -> None:
    """Write content to file and chown it to the real user (handles sudo context)."""
    from pathlib import Path

    from wexample_helpers.helpers.user import user_get_real_gid, user_get_real_uid

    p = Path(file_path)
    p.write_text(content, encoding=encoding)
    os.chmod(p, mode)
    os.chown(p, user_get_real_uid(), user_get_real_gid())


def file_mkdir_as_real_user(path: PathOrString, mode: int = 0o755) -> None:
    """Create directory (and parents) and chown all newly created dirs to the real user."""
    from pathlib import Path

    from wexample_helpers.helpers.user import user_get_real_gid, user_get_real_uid

    p = Path(path)

    # Collect all dirs that don't exist yet, from deepest to shallowest
    to_create = []
    current = p
    while not current.exists():
        to_create.append(current)
        current = current.parent

    p.mkdir(parents=True, exist_ok=True)

    uid, gid = user_get_real_uid(), user_get_real_gid()
    for created in to_create:
        os.chmod(created, mode)
        os.chown(created, uid, gid)


def file_write_ensure(
    file_path: FileStringOrPath, content: str, encoding: str = "utf-8"
) -> None:
    """
    Write content to file, creating parent directories if needed.

    :param file_path: Destination file path.
    :param content: Text content to write.
    :param encoding: Text encoding.
    """
    p = file_resolve_path(file_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding=encoding)
