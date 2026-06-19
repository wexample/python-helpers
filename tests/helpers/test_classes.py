from __future__ import annotations


def test_classes_get_definition_path_returns_source_file() -> None:
    from wexample_helpers.helper.classes import classes_get_definition_path

    class Sample:
        pass

    path = classes_get_definition_path(Sample())

    assert str(path).endswith("test_classes.py")
