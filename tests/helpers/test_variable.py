from __future__ import annotations


def test_copy_shallow_dict_returns_new_dict() -> None:
    from wexample_helpers.helpers.variable import copy_shallow

    original = {"a": 1}
    copy = copy_shallow(original)

    assert copy == original
    assert copy is not original


def test_copy_shallow_immutable_returns_same_object() -> None:
    from wexample_helpers.helpers.variable import copy_shallow

    assert copy_shallow(42) == 42
    assert copy_shallow("hello") == "hello"
    assert copy_shallow(None) is None


def test_copy_shallow_is_shallow_not_deep() -> None:
    from wexample_helpers.helpers.variable import copy_shallow

    inner = [1, 2]
    original = [inner]
    copy = copy_shallow(original)

    assert copy[0] is inner


def test_copy_shallow_list_returns_new_list() -> None:
    from wexample_helpers.helpers.variable import copy_shallow

    original = [1, 2, 3]
    copy = copy_shallow(original)

    assert copy == original
    assert copy is not original


def test_copy_shallow_set_returns_new_set() -> None:
    from wexample_helpers.helpers.variable import copy_shallow

    original = {1, 2, 3}
    copy = copy_shallow(original)

    assert copy == original
    assert copy is not original


def test_copy_shallow_tuple_returns_equal_tuple() -> None:
    from wexample_helpers.helpers.variable import copy_shallow

    original = (1, 2, 3)
    copy = copy_shallow(original)

    assert copy == original
