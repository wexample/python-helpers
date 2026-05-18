"""
Benchmarks for wexample_helpers critical path.

Run with:
    pytest benchmarks/test_benchmark.py --benchmark-only

Hot paths targeted:
- string helpers: _normalize (called by every case converter), case conversion, detect_case
- dict helpers: path traversal, deep merge, interpolation
- type helpers: generic value validation
"""

from __future__ import annotations

from wexample_helpers.helpers.dict import (
    dict_get_item_by_path,
    dict_has_item_by_path,
    dict_interpolate,
    dict_merge,
    dict_set_item_by_path,
)
from wexample_helpers.helpers.string import (
    _normalize,
    string_detect_case,
    string_remove_prefix,
    string_replace_params,
    string_to_camel_case,
    string_to_kebab_case,
    string_to_pascal_case,
    string_to_snake_case,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_SNAKE = "my_example_string"
_KEBAB = "my-example-string"
_PASCAL = "MyExampleString"
_CAMEL = "myExampleString"
_CONSTANT = "MY_EXAMPLE_STRING"
_LONG_SNAKE = "this_is_a_very_long_snake_case_identifier_used_in_deployment"
_MIXED = "myPackage_Name-With/mixed.separators"

_SHALLOW_DICT = {"name": "test", "version": "1.0.0", "active": True, "count": 42}
_DEEP_DICT = {
    "app": {
        "server": {"host": "localhost", "port": 8080},
        "database": {"url": "postgres://localhost/db", "pool_size": 10},
    },
    "logging": {"level": "INFO"},
}
_INTERP_DICT = {
    "path": "/home/${user}/projects/${project}",
    "url": "https://${host}:${port}/api",
    "nested": {"key": "${value}"},
}
_INTERP_VARS = {"user": "weeger", "project": "wex", "host": "localhost", "port": "8080", "value": "hello"}

_DICT_A = {"a": 1, "b": {"x": 10, "y": 20}, "c": [1, 2, 3]}
_DICT_B = {"b": {"y": 99, "z": 30}, "d": 4}
_DICT_C = {"a": 100, "b": {"x": 0}, "e": {"f": 5}}


# ---------------------------------------------------------------------------
# string._normalize — called by every case converter; this is the inner loop
# ---------------------------------------------------------------------------


def test_normalize_snake(benchmark):
    """Normalize a snake_case string — separator split path."""
    benchmark(_normalize, _SNAKE)


def test_normalize_pascal(benchmark):
    """Normalize a PascalCase string — camelCase split via regex."""
    benchmark(_normalize, _PASCAL)


def test_normalize_mixed(benchmark):
    """Normalize a mixed-separator string — exercises all regex branches."""
    benchmark(_normalize, _MIXED)


def test_normalize_long(benchmark):
    """Normalize a long snake_case identifier — stresses the split loop."""
    benchmark(_normalize, _LONG_SNAKE)


# ---------------------------------------------------------------------------
# string case converters — each calls _normalize then joins
# ---------------------------------------------------------------------------


def test_to_snake_case(benchmark):
    benchmark(string_to_snake_case, _PASCAL)


def test_to_kebab_case(benchmark):
    benchmark(string_to_kebab_case, _PASCAL)


def test_to_pascal_case(benchmark):
    benchmark(string_to_pascal_case, _SNAKE)


def test_to_camel_case(benchmark):
    benchmark(string_to_camel_case, _SNAKE)


def test_to_snake_case_long(benchmark):
    """Longer input — stresses _normalize regex on a realistic identifier."""
    benchmark(string_to_snake_case, _LONG_SNAKE)


# ---------------------------------------------------------------------------
# string_detect_case — 9 sequential regex patterns, called on every check
# ---------------------------------------------------------------------------


def test_detect_case_snake(benchmark):
    """First match exits early (constant check), snake is second."""
    benchmark(string_detect_case, _SNAKE)


def test_detect_case_pascal(benchmark):
    """Pascal exits at 7th pattern — near worst-case."""
    benchmark(string_detect_case, _PASCAL)


def test_detect_case_mixed(benchmark):
    """Mixed falls through all patterns — actual worst-case."""
    benchmark(string_detect_case, _MIXED)


# ---------------------------------------------------------------------------
# string_remove_prefix — currently uses re.sub instead of str.removeprefix
# ---------------------------------------------------------------------------


def test_remove_prefix_match(benchmark):
    """Prefix is present — re.sub performs the substitution."""
    benchmark(string_remove_prefix, "wexample_helpers", "wexample_")


def test_remove_prefix_no_match(benchmark):
    """Prefix absent — re.sub still compiles and searches."""
    benchmark(string_remove_prefix, "other_module", "wexample_")


# ---------------------------------------------------------------------------
# string_replace_params — called when rendering templates
# ---------------------------------------------------------------------------


def test_replace_params(benchmark):
    benchmark(
        string_replace_params,
        "Package %vendor%_%name% version %version% at %path%",
        {"vendor": "wexample", "name": "helpers", "version": "1.0.0", "path": "/src"},
    )


# ---------------------------------------------------------------------------
# dict_get_item_by_path — called on every config read
# ---------------------------------------------------------------------------


def test_dict_get_depth_1(benchmark):
    benchmark(dict_get_item_by_path, _DEEP_DICT, "app")


def test_dict_get_depth_2(benchmark):
    benchmark(dict_get_item_by_path, _DEEP_DICT, "app.server")


def test_dict_get_depth_3(benchmark):
    benchmark(dict_get_item_by_path, _DEEP_DICT, "app.server.host")


def test_dict_get_missing(benchmark):
    """Key doesn't exist — exercises the default return path."""
    benchmark(dict_get_item_by_path, _DEEP_DICT, "app.server.nonexistent")


# ---------------------------------------------------------------------------
# dict_has_item_by_path — existence check before access
# ---------------------------------------------------------------------------


def test_dict_has_depth_3_hit(benchmark):
    benchmark(dict_has_item_by_path, _DEEP_DICT, "app.server.host")


def test_dict_has_depth_3_miss(benchmark):
    benchmark(dict_has_item_by_path, _DEEP_DICT, "app.server.missing")


# ---------------------------------------------------------------------------
# dict_set_item_by_path — config writes during deployment
# ---------------------------------------------------------------------------


def test_dict_set_depth_1(benchmark):
    def _set():
        d = dict(_SHALLOW_DICT)
        dict_set_item_by_path(d, "name", "updated")

    benchmark(_set)


def test_dict_set_depth_3(benchmark):
    def _set():
        d = {"app": {"server": {"port": 8080}}}
        dict_set_item_by_path(d, "app.server.port", 443)

    benchmark(_set)


# ---------------------------------------------------------------------------
# dict_merge — recursive merge; called during config assembly
# ---------------------------------------------------------------------------


def test_dict_merge_two_shallow(benchmark):
    benchmark(dict_merge, _DICT_A, _DICT_B)


def test_dict_merge_three_dicts(benchmark):
    benchmark(dict_merge, _DICT_A, _DICT_B, _DICT_C)


def test_dict_merge_nested(benchmark):
    """Deep nested merge — exercises the recursive branch."""
    a = {"x": {"y": {"z": 1, "w": 2}}}
    b = {"x": {"y": {"z": 99, "v": 3}}}
    benchmark(dict_merge, a, b)


# ---------------------------------------------------------------------------
# dict_interpolate — regex compiled inside function on every call (!)
# ---------------------------------------------------------------------------


def test_dict_interpolate_flat_string(benchmark):
    """Single string with two variables."""
    benchmark(dict_interpolate, "/home/${user}/${project}", _INTERP_VARS)


def test_dict_interpolate_nested_dict(benchmark):
    """Full nested dict — exercises recursive traversal + regex per value."""
    benchmark(dict_interpolate, _INTERP_DICT, _INTERP_VARS)


def test_dict_interpolate_no_vars(benchmark):
    """No substitution needed — measures baseline regex overhead."""
    benchmark(dict_interpolate, "plain string with no variables", _INTERP_VARS)


# ---------------------------------------------------------------------------
# type_generic_value_is_valid — called by attrs validators on every set
# ---------------------------------------------------------------------------


def test_type_validate_simple_str(benchmark):
    from wexample_helpers.helpers.type import type_generic_value_is_valid

    benchmark(type_generic_value_is_valid, "hello", str)


def test_type_validate_union(benchmark):
    """Union[str, int] — iterates over args until match."""
    from typing import Union

    from wexample_helpers.helpers.type import type_generic_value_is_valid

    benchmark(type_generic_value_is_valid, 42, Union[str, int])


def test_type_validate_optional(benchmark):
    """Optional[str] (= Union[str, None]) — common in attrs fields."""
    from typing import Optional

    from wexample_helpers.helpers.type import type_generic_value_is_valid

    benchmark(type_generic_value_is_valid, "value", Optional[str])


def test_type_validate_list_of_str(benchmark):
    from wexample_helpers.helpers.type import type_generic_value_is_valid

    benchmark(type_generic_value_is_valid, ["a", "b", "c"], list[str])
