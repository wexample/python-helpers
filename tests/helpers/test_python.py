from __future__ import annotations


def test_python_get_return_type_from_annotations_missing_returns_none() -> None:
    from wexample_helpers.helpers.python import (
        python_get_return_type_from_annotations,
    )

    def func(a):
        return a

    assert python_get_return_type_from_annotations(func) is None


def test_python_get_return_type_from_annotations_named_type() -> None:
    from wexample_helpers.helpers.python import (
        python_get_return_type_from_annotations,
    )

    def func() -> int:
        return 1

    assert python_get_return_type_from_annotations(func) == "int"


def test_python_get_return_type_from_annotations_typing_type() -> None:
    pass

    from wexample_helpers.helpers.python import (
        python_get_return_type_from_annotations,
    )

    def func() -> int | None:
        return None

    result = python_get_return_type_from_annotations(func)
    assert result is not None
    assert "typing." not in result


def test_python_get_return_type_from_docstring_arrow() -> None:
    from wexample_helpers.helpers.python import (
        python_get_return_type_from_docstring,
    )

    assert python_get_return_type_from_docstring("Does -> str things") == "str"


def test_python_get_return_type_from_docstring_none_when_empty() -> None:
    from wexample_helpers.helpers.python import (
        python_get_return_type_from_docstring,
    )

    assert python_get_return_type_from_docstring(None) is None
    assert python_get_return_type_from_docstring("") is None


def test_python_get_return_type_from_docstring_none_when_no_match() -> None:
    from wexample_helpers.helpers.python import (
        python_get_return_type_from_docstring,
    )

    assert python_get_return_type_from_docstring("plain text") is None


def test_python_get_return_type_from_docstring_returns_keyword() -> None:
    from wexample_helpers.helpers.python import (
        python_get_return_type_from_docstring,
    )

    assert python_get_return_type_from_docstring("Returns int value") == "int"
