from __future__ import annotations

from pathlib import Path


def test_render_template_falls_back_to_second_path(tmp_path: Path) -> None:
    from wexample_helpers.helpers.jinja import render_template

    primary = tmp_path / "primary"
    fallback = tmp_path / "fallback"
    primary.mkdir()
    fallback.mkdir()
    (fallback / "only.j2").write_text("from fallback")

    result = render_template("only.j2", search_paths=[primary, fallback])
    assert result == "from fallback"


def test_render_template_first_search_path_wins(tmp_path: Path) -> None:
    from wexample_helpers.helpers.jinja import render_template

    primary = tmp_path / "primary"
    fallback = tmp_path / "fallback"
    primary.mkdir()
    fallback.mkdir()
    (primary / "t.j2").write_text("primary")
    (fallback / "t.j2").write_text("fallback")

    result = render_template("t.j2", search_paths=[primary, fallback])
    assert result == "primary"


def test_render_template_ignores_non_directory_paths(tmp_path: Path) -> None:
    from wexample_helpers.helpers.jinja import render_template

    real = tmp_path / "real"
    real.mkdir()
    (real / "x.j2").write_text("ok")

    result = render_template("x.j2", search_paths=[tmp_path / "missing", real])
    assert result == "ok"


def test_render_template_renders_context(tmp_path: Path) -> None:
    from wexample_helpers.helpers.jinja import render_template

    (tmp_path / "greet.j2").write_text("Hello {{ name }}!")
    result = render_template("greet.j2", {"name": "World"}, [tmp_path])
    assert result == "Hello World!"
