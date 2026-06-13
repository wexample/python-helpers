from __future__ import annotations

from pathlib import Path


def test_path_rebase_accepts_string_arguments(tmp_path: Path) -> None:
    from wexample_helpers.helpers.path import path_rebase

    root_src = tmp_path / "a"
    root_dest = tmp_path / "b"
    (root_src).mkdir()
    (root_dest).mkdir()
    file_src = root_src / "f.txt"
    file_src.write_text("x")

    result = path_rebase(str(root_src), str(file_src), str(root_dest))

    assert result == str(root_dest / "f.txt")


def test_path_rebase_moves_path_to_new_root(tmp_path: Path) -> None:
    from wexample_helpers.helpers.path import path_rebase

    root_src = tmp_path / "project"
    root_dest = tmp_path / "html"
    nested = root_src / "src"
    nested.mkdir(parents=True)
    (root_dest).mkdir()
    file_src = nested / "test.php"
    file_src.write_text("x")

    result = path_rebase(root_src, file_src, root_dest)

    assert result == str(root_dest / "src" / "test.php")
