from types import NoneType
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union
from collections.abc import Callable

from wexample_helpers.helpers.type import type_is_compatible, type_is_generic
from wexample_helpers.test.abstract_test_helpers import AbstractTestHelpers


class TestHelperType(AbstractTestHelpers):
    def test_type_is_generic(self) -> None:
        # Types that should be detected as generic
        should_be_true = [
            list,
            list,
            dict,
            dict,
            tuple,
            tuple,
            Union,
            list[str],
            dict[str, Any],
            Union[list[int], dict[int, int]],
        ]

        # Types that should NOT be detected as generic
        should_not_be_true = [
            int,
            str,
            float,
            bool,
            complex,
            Any,  # Any is not considered a generic type here
            None,  # NoneType is also non-generic
            object,
            type,  # Built-in 'type' itself is not a generic
        ]

        for type_ in should_be_true:
            assert type_is_generic(
                type_
            ), f"{type_} should be detected as a generic type"

        for type_ in should_not_be_true:
            assert not type_is_generic(
                type_
            ), f"{type_} should NOT be detected as a generic type"

    def test_type_is_compatibility(self) -> None:
        success_cases = [
            (str, Any),
            (bool, Any),
            (str, str),
            (int, int),
            (float, float),
            (type(None), type(None)),  # NoneType
            (list, list),
            (list, list),
            (dict, dict),
            (dict, dict),
            (dict[str, str], dict[Any, Any]),
            (dict[str, int], dict[str, int]),
            (str, Union[str, dict[str, Any]]),
            (Callable[..., bool], Callable),
            (Callable[..., bool], Callable),
            (Callable[..., Any], Callable[..., Any]),
            (Callable[..., bool], Callable[..., bool]),
            (Callable[..., bool], Callable[..., bool]),
            (Callable[..., Callable[..., str]], Callable[..., Callable]),
        ]

        failure_cases = [
            (int, str),
            (str, int),
            (type(None), int),  # NoneType incompatible with int
            (dict, list),
            (list, dict),
            (dict[str, int], dict[str, str]),
            (int, Union[str, dict[str, Any]]),
            (Callable[..., bool], Callable[..., str]),
        ]

        for actual_type, expected_type in success_cases:
            assert type_is_compatible(
                actual_type, expected_type
            ), f"Expected {actual_type} to be compatible with {expected_type}"

        for actual_type, expected_type in failure_cases:
            assert not type_is_compatible(
                actual_type, expected_type
            ), f"Expected {actual_type} to be incompatible with {expected_type}"

    def test_validation(self) -> bool:
        def _test_callable() -> bool:
            return True

        class TestClassA:
            pass

        class TestClassB(TestClassA):
            pass

        self._test_type_validate_or_fail(
            success_cases=[
                # Basic types
                ("str", Any),
                (True, Any),
                ("str", str),
                (123, int),
                (123.123, float),
                (None, NoneType),
                # Basic containers
                ([], list),
                ([], list),
                ({}, dict),
                ({}, dict),
                # Typed containers
                (["item1", "item2"], list[str]),
                ([1, 2, 3], list[int]),
                ({"lorem": "ipsum"}, dict[str, str]),
                ({"lorem": 123}, dict[str, int]),
                ([TestClassA(), TestClassB()], list[TestClassA]),
                # Union and Optional
                (None, Optional[str]),
                ("hello", Union[str, int]),
                (123, Union[str, int]),
                ({"key": "value"}, Union[str, dict[str, str]]),
                (None, Union[str, NoneType]),
                ("optional", Optional[str]),
                # Callable
                (_test_callable, Callable),
                (_test_callable, Callable[..., Any]),
                (_test_callable, Callable[..., bool]),
                # Tuples and Sets
                ((1, "str"), tuple[int, str]),
                ({"apple", "banana"}, set[str]),
                ({1, 2, 3}, set[int]),
                # Nested types
                ({"nested": {"key": "value"}}, dict[str, dict[str, str]]),
                ([{"key": 1}, {"key": 2}], list[dict[str, int]]),
                (({"key": "value"}, 123), tuple[dict[str, str], int]),
                # Classes and types
                (TestClassA(), TestClassA),
                (TestClassB(), TestClassA),  # Compatibility with superclass
                (TestClassB(), TestClassB),
                # Class types
                (TestClassA, type[TestClassA]),
                (TestClassB, type[TestClassA]),
                (TestClassB, type[TestClassB]),
                (TestClassA, type),
                (TestClassB, type),
                # Nested Unions and Optionals
                ({"key": "value"}, Union[dict[str, str], list[str]]),
                ([1, 2, 3], Union[list[int], set[int]]),
                ({"key": "value"}, Union[dict[str, str], NoneType]),
                (None, Union[dict[str, str], NoneType]),
                (123, Union[Optional[int], NoneType]),
                (TestClassB(), Union[TestClassA, TestClassB]),
                (TestClassB(), Union[TestClassA, str]),
                (TestClassB, Union[type[TestClassA], type[TestClassB]]),
            ],
            failure_cases=[
                # Type mismatches
                (123, str),
                ("123", int),
                (None, int),
                # Container type mismatches
                ({}, list),
                ([], dict),
                ({"lorem": 123}, dict[str, str]),
                # Union mismatches
                (123, Union[str, dict[str, Any]]),
                ("not_callable", Callable[..., str]),
                # Callable with incompatible signature
                (_test_callable, Callable[..., str]),
                # Class type mismatches
                (
                    TestClassA(),
                    TestClassB,
                ),  # TestClassA instance is not compatible with TestClassB type
                (123, TestClassA),
                ("str", TestClassB),
                # Type mismatches for class types
                (
                    TestClassA(),
                    type[TestClassA],
                ),  # TestClassA() is an instance, not a type
                (TestClassB(), type),
                # Non-type values for Type
                (123, type),
                ("str", type),
                # Incorrect nested types
                ([1, "str"], list[int]),
                ({"key": 123}, dict[str, str]),
                ({"key": "value"}, list[dict[str, str]]),  # Expecting List, got Dict
                (["str"], set[str]),  # List vs. Set
                # Incorrect Optional and Union usage
                (123, Optional[str]),  # Expecting str or None
                (None, int),  # NoneType mismatch
                # Tuple and Set mismatches
                ((1, "str"), tuple[str, int]),  # Type order mismatch in Tuple
                ({"apple", 1}, set[str]),  # Mixed types in Set
                (TestClassA, Union[int, str, float]),
                (TestClassA, Union[TestClassB]),
                (TestClassA, TestClassB),
                (TestClassA, TestClassA),
            ],
        )
