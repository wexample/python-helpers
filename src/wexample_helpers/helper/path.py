from __future__ import annotations

from pathlib import Path


def path_rebase(
    root_src: str | Path, path_src: str | Path, root_dest: str | Path
) -> str:
    """
    Rebase a path from one root to another.

    Example:
        root_src="/home/me/project"
        path_src="/home/me/project/src/test.php"
        root_dest="/var/www/html"

        → "/var/www/html/src/test.php"
    """
    root_src = Path(root_src).resolve()
    path_src = Path(path_src).resolve()

    return str(Path(root_dest) / path_src.relative_to(root_src))
