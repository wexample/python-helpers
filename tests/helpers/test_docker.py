from __future__ import annotations

from pathlib import Path


def test_docker_build_name_from_path_differs_per_path(tmp_path: Path) -> None:
    from wexample_helpers.helpers.docker import docker_build_name_from_path

    a = docker_build_name_from_path(tmp_path / "a", "img")
    b = docker_build_name_from_path(tmp_path / "b", "img")
    assert a != b


def test_docker_build_name_from_path_is_deterministic(tmp_path: Path) -> None:
    from wexample_helpers.helpers.docker import docker_build_name_from_path

    first = docker_build_name_from_path(tmp_path, "myimage")
    second = docker_build_name_from_path(tmp_path, "myimage")
    assert first == second


def test_docker_build_name_from_path_uses_prefix_and_image(tmp_path: Path) -> None:
    from wexample_helpers.helpers.docker import docker_build_name_from_path

    name = docker_build_name_from_path(tmp_path, "myimage", prefix="wex")
    assert name.startswith("wex-myimage-")
