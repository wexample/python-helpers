from __future__ import annotations


def test_error_format_returns_string_for_exception() -> None:
    from wexample_helpers.helpers.error import error_format

    try:
        raise ValueError("boom")
    except ValueError as exc:
        result = error_format(exc)

    assert isinstance(result, str)
    assert "boom" in result


def test_error_get_truncate_index_returns_int() -> None:
    from wexample_helpers.helpers.error import error_get_truncate_index

    error = ValueError("x")
    result = error_get_truncate_index([], error)

    assert isinstance(result, int)
