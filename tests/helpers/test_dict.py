from __future__ import annotations

import pytest


def test_dict_get_first_missing_key() -> None:
    from wexample_helpers.helpers.dict import dict_get_first_missing_key

    data = {"a": 1, "b": 2}
    assert dict_get_first_missing_key(data, ["a", "b", "c"]) == "c"
    assert dict_get_first_missing_key(data, ["a", "b"]) is None


def test_dict_get_item_by_path() -> None:
    from wexample_helpers.helpers.dict import dict_get_item_by_path

    data = {"a": {"b": {"c": 1}}}
    assert dict_get_item_by_path(data, "a.b.c") == 1
    assert dict_get_item_by_path(data, "a.b.d") is None
    assert dict_get_item_by_path(data, "x.y", default=42) == 42


def test_dict_has_item_by_path() -> None:
    from wexample_helpers.helpers.dict import dict_has_item_by_path

    data = {"a": {"b": {"c": 1}}}
    assert dict_has_item_by_path(data, "a.b.c") is True
    assert dict_has_item_by_path(data, "a.b.d") is False
    assert dict_has_item_by_path(data, "x.y") is False


def test_dict_interpolate_flattens_full_var_list_in_list() -> None:
    from wexample_helpers.helpers.dict import dict_interpolate

    assert dict_interpolate(["${L}", "x"], {"L": ["a", "b"]}) == ["a", "b", "x"]


def test_dict_interpolate_full_var_returns_list_as_is() -> None:
    from wexample_helpers.helpers.dict import dict_interpolate

    assert dict_interpolate("${L}", {"L": [1, 2]}) == [1, 2]


def test_dict_interpolate_full_var_returns_scalar() -> None:
    from wexample_helpers.helpers.dict import dict_interpolate

    assert dict_interpolate("${FOO}", {"FOO": "bar"}) == "bar"


def test_dict_interpolate_inline_non_scalar_raises() -> None:
    from wexample_helpers.helpers.dict import dict_interpolate

    with pytest.raises(ValueError, match="Cannot interpolate non-scalar variable"):
        dict_interpolate("${L}/sub", {"L": [1, 2]})


def test_dict_interpolate_inline_substitution() -> None:
    from wexample_helpers.helpers.dict import dict_interpolate

    assert dict_interpolate("${LOCAL}/wex", {"LOCAL": "/p"}) == "/p/wex"


def test_dict_interpolate_inline_unknown_stays_literal() -> None:
    from wexample_helpers.helpers.dict import dict_interpolate

    assert dict_interpolate("a/${X}/b", {}) == "a/${X}/b"


def test_dict_interpolate_passes_through_non_containers() -> None:
    from wexample_helpers.helpers.dict import dict_interpolate

    assert dict_interpolate(42, {}) == 42


def test_dict_interpolate_recurses_into_dict() -> None:
    from wexample_helpers.helpers.dict import dict_interpolate

    assert dict_interpolate({"k": "${FOO}"}, {"FOO": "bar"}) == {"k": "bar"}


def test_dict_interpolate_unknown_full_var_stays_literal() -> None:
    from wexample_helpers.helpers.dict import dict_interpolate

    assert dict_interpolate("${UNKNOWN}", {}) == "${UNKNOWN}"


def test_dict_merge() -> None:
    from wexample_helpers.helpers.dict import dict_merge

    dict1 = {"a": 1, "b": {"c": 2}}
    dict2 = {"b": {"d": 3}, "e": 4}
    merged = dict_merge(dict1, dict2)
    assert merged == {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}


def test_dict_remove_item_by_path() -> None:
    from wexample_helpers.helpers.dict import dict_remove_item_by_path

    data = {"a": {"b": {"c": 1, "d": 2}}}
    dict_remove_item_by_path(data, "a.b.c")
    assert data == {"a": {"b": {"d": 2}}}

    # Test removing non-existent path
    dict_remove_item_by_path(data, "x.y.z")
    assert data == {"a": {"b": {"d": 2}}}


def test_dict_set_item_by_path() -> None:
    from wexample_helpers.helpers.dict import dict_set_item_by_path

    data = {}
    dict_set_item_by_path(data, "a.b.c", 1)
    assert data == {"a": {"b": {"c": 1}}}

    # Test merge behavior
    dict_set_item_by_path(data, "a.b", {"d": 2}, when_exist="merge")
    assert data == {"a": {"b": {"c": 1, "d": 2}}}


def test_dict_sort_values() -> None:
    from wexample_helpers.helpers.dict import dict_sort_values

    data = {"c": 3, "a": 1, "b": 2}
    sorted_dict = dict_sort_values(data)
    assert list(sorted_dict.items()) == [("a", 1), ("b", 2), ("c", 3)]
