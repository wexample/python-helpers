from __future__ import annotations

import pytest


def test_is_greater_than_equal_respects_flag() -> None:
    from wexample_helpers.helper.version import is_greater_than, version_parse

    a = version_parse("1.2.3")
    b = version_parse("1.2.3")
    assert is_greater_than(a, b, true_if_equal=False) is False
    assert is_greater_than(a, b, true_if_equal=True) is True


def test_is_greater_than_major() -> None:
    from wexample_helpers.helper.version import is_greater_than, version_parse

    assert is_greater_than(version_parse("2.0.0"), version_parse("1.9.9")) is True
    assert is_greater_than(version_parse("1.0.0"), version_parse("2.0.0")) is False


def test_version_increment_intermediate_resets_minor() -> None:
    from wexample_helpers.helper.version import version_increment

    assert version_increment("1.2.3", "intermediate") == "1.3.0"


def test_version_increment_major_resets_lower() -> None:
    from wexample_helpers.helper.version import version_increment

    assert version_increment("1.2.3", "major") == "2.0.0"


def test_version_increment_minor() -> None:
    from wexample_helpers.helper.version import version_increment

    assert version_increment("1.2.3", "minor") == "1.2.4"


def test_version_increment_pre_build() -> None:
    from wexample_helpers.helper.version import version_increment

    assert version_increment("1.2.3", "alpha") == "1.2.3-alpha.1"


def test_version_increment_raises_on_invalid() -> None:
    from wexample_helpers.helper.version import version_increment

    with pytest.raises(ValueError, match=r"Invalid version format"):
        version_increment("not-a-version", "minor")


def test_version_join_basic() -> None:
    from wexample_helpers.helper.version import version_join

    version = {
        "major": 1,
        "intermediate": 2,
        "minor": 3,
        "pre_build_type": None,
        "pre_build_number": None,
    }
    assert version_join(version) == "1.2.3"


def test_version_join_with_pre_build() -> None:
    from wexample_helpers.helper.version import version_join

    version = {
        "major": 1,
        "intermediate": 2,
        "minor": 3,
        "pre_build_type": "beta",
        "pre_build_number": 4,
    }
    assert version_join(version) == "1.2.3-beta.4"


def test_version_join_with_string_build() -> None:
    from wexample_helpers.helper.version import version_join

    version = {
        "major": 1,
        "intermediate": 2,
        "minor": 3,
        "pre_build_type": None,
        "pre_build_number": None,
    }
    assert version_join(version, add_build="xyz") == "1.2.3+build.xyz"


def test_version_parse_basic() -> None:
    from wexample_helpers.helper.version import version_parse

    result = version_parse("1.2.3")
    assert result == {
        "major": 1,
        "intermediate": 2,
        "minor": 3,
        "pre_build_type": None,
        "pre_build_number": None,
    }


def test_version_parse_pre_build() -> None:
    from wexample_helpers.helper.version import version_parse

    result = version_parse("1.2.3-beta.4")
    assert result is not None
    assert result["pre_build_type"] == "beta"
    assert result["pre_build_number"] == 4


def test_version_parse_pre_build_with_build_metadata() -> None:
    from wexample_helpers.helper.version import version_parse

    result = version_parse("1.2.3-beta.4+build.1234")
    assert result is not None
    assert result["pre_build_number"] == 4


def test_version_parse_returns_none_on_empty() -> None:
    from wexample_helpers.helper.version import version_parse

    assert version_parse("") is None


def test_version_parse_returns_none_on_non_numeric() -> None:
    from wexample_helpers.helper.version import version_parse

    assert version_parse("abc") is None
