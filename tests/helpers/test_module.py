from __future__ import annotations

import sys
from pathlib import Path

import pytest

_MODULE_SOURCE = """
class Alpha:
    pass


class Beta:
    pass
"""


def _write_module(tmp_path: Path) -> Path:
    file_path = tmp_path / "sample_module.py"
    file_path.write_text(_MODULE_SOURCE)
    return file_path


def test_ensure_sys_path_is_idempotent(tmp_path: Path) -> None:
    from wexample_helpers.helpers.module import ensure_sys_path

    target = tmp_path / "some_dir"
    s = str(target)
    try:
        ensure_sys_path(target)
        ensure_sys_path(target)
        assert sys.path.count(s) == 1
    finally:
        while s in sys.path:
            sys.path.remove(s)


def test_module_are_same_identity() -> None:
    from wexample_helpers.helpers.module import module_are_same

    class Foo:
        pass

    assert module_are_same(Foo, Foo) is True


def test_module_are_same_returns_false_for_non_types() -> None:
    from wexample_helpers.helpers.module import module_are_same

    assert module_are_same(1, 2) is False


def test_module_are_same_distinct_classes() -> None:
    from wexample_helpers.helpers.module import module_are_same

    class Foo:
        pass

    class Bar:
        pass

    assert module_are_same(Foo, Bar) is False


def test_module_build_fqmn_from_paths_with_package_name(tmp_path: Path) -> None:
    from wexample_helpers.helpers.module import module_build_fqmn_from_paths

    file_path = tmp_path / "b" / "c.py"
    file_path.parent.mkdir(parents=True)
    file_path.write_text("x")

    result = module_build_fqmn_from_paths(file_path, tmp_path, "pkg")
    assert result == "pkg.b.c"


def test_module_build_fqmn_from_paths_without_package_name(tmp_path: Path) -> None:
    from wexample_helpers.helpers.module import module_build_fqmn_from_paths

    file_path = tmp_path / "b" / "c.py"
    file_path.parent.mkdir(parents=True)
    file_path.write_text("x")

    result = module_build_fqmn_from_paths(file_path, tmp_path)
    assert result == "b.c"


def test_module_load_class_from_file_loads_class(tmp_path: Path) -> None:
    from wexample_helpers.helpers.module import module_load_class_from_file

    file_path = _write_module(tmp_path)
    cls = module_load_class_from_file(file_path, "Alpha")
    assert cls.__name__ == "Alpha"


def test_module_load_class_from_file_missing_file(tmp_path: Path) -> None:
    from wexample_helpers.helpers.module import module_load_class_from_file

    with pytest.raises(FileNotFoundError, match=r"Module file not found"):
        module_load_class_from_file(tmp_path / "nope.py", "Alpha")


def test_module_load_class_from_file_missing_class(tmp_path: Path) -> None:
    from wexample_helpers.helpers.module import module_load_class_from_file

    file_path = _write_module(tmp_path)
    with pytest.raises(ImportError, match=r"not found in module"):
        module_load_class_from_file(file_path, "Missing")


def test_module_load_class_from_file_if_exist_returns_none_on_failure(
    tmp_path: Path,
) -> None:
    from wexample_helpers.helpers.module import (
        module_load_class_from_file_if_exist,
    )

    result = module_load_class_from_file_if_exist(
        file_path=tmp_path / "nope.py", class_name="Alpha"
    )
    assert result is None


def test_module_collect_classes_returns_module_classes(tmp_path: Path) -> None:
    from wexample_helpers.helpers.module import (
        module_collect_classes,
        module_load_class_from_file,
    )

    file_path = _write_module(tmp_path)
    cls = module_load_class_from_file(file_path, "Alpha")
    module = sys.modules[cls.__module__]

    collected = module_collect_classes(module)
    assert set(collected) == {"Alpha", "Beta"}


def test_module_get_distribution_map_returns_lowercase_keys() -> None:
    from wexample_helpers.helpers.module import module_get_distribution_map

    result = module_get_distribution_map()
    assert isinstance(result, dict)
    assert all(key == key.lower() for key in result)


def test_module_get_path_returns_existing_path() -> None:
    import wexample_helpers

    from wexample_helpers.helpers.module import module_get_path

    path = module_get_path(wexample_helpers)
    assert path.exists()
