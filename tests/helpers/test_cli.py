from __future__ import annotations


def test_cli_argument_convert_value_bool_truthy() -> None:
    from wexample_helpers.helpers.cli import cli_argument_convert_value

    assert cli_argument_convert_value("yes", bool) is True
    assert cli_argument_convert_value("1", bool) is True
    assert cli_argument_convert_value("no", bool) is False


def test_cli_argument_convert_value_int() -> None:
    from wexample_helpers.helpers.cli import cli_argument_convert_value

    assert cli_argument_convert_value("42", int) == 42


def test_cli_argument_convert_value_float() -> None:
    from wexample_helpers.helpers.cli import cli_argument_convert_value

    assert cli_argument_convert_value("3.5", float) == 3.5


def test_cli_argument_convert_value_str() -> None:
    from wexample_helpers.helpers.cli import cli_argument_convert_value

    assert cli_argument_convert_value("hello", str) == "hello"


def test_cli_argument_convert_value_list_splits_on_comma() -> None:
    from wexample_helpers.helpers.cli import cli_argument_convert_value

    assert cli_argument_convert_value("a, b ,c", list) == ["a", "b", "c"]


def test_cli_argument_convert_value_custom_type_uses_constructor() -> None:
    from wexample_helpers.helpers.cli import cli_argument_convert_value

    class Wrapper:
        def __init__(self, value: str) -> None:
            self.value = value

    result = cli_argument_convert_value("x", Wrapper)
    assert isinstance(result, Wrapper)
    assert result.value == "x"


def test_cli_make_clickable_path_full_path() -> None:
    from wexample_helpers.helpers.cli import cli_make_clickable_path

    result = cli_make_clickable_path("/tmp/file.txt")
    assert "file://" in result
    assert "/tmp/file.txt" in result


def test_cli_make_clickable_path_short_title_uses_basename() -> None:
    from wexample_helpers.helpers.cli import cli_make_clickable_path

    result = cli_make_clickable_path("/tmp/dir/file.txt", short_title=True)
    assert "file.txt" in result
    assert "dir/file.txt" not in result.split("\033\\")[1]


def test_cli_make_clickable_path_custom_title() -> None:
    from wexample_helpers.helpers.cli import cli_make_clickable_path

    result = cli_make_clickable_path("/tmp/file.txt", short_title="Open me")
    assert "Open me" in result
