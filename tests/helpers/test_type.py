from types import NoneType
from typing import Any, Callable, Dict, List, Tuple, Union, Type, Optional, Set

from wexample_helpers.helpers.type import (
    type_is_compatible,
    type_is_generic,
)

from wexample_helpers.test.abstract_test_helpers import AbstractTestHelpers

class TestHelperType(AbstractTestHelpers):
    def test_type_is_generic(self):
        # Types that should be detected as generic
        should_be_true = [
            list,
            List,
            dict,
            Dict,
            tuple,
            Tuple,
            Union,
            List[str],
            Dict[str, Any],
            Union[List[int], Dict[int, int]],
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

    def test_type_is_compatibility(self):
        success_cases = [
            (str, Any),
            (bool, Any),
            (str, str),
            (int, int),
            (float, float),
            (type(None), type(None)),  # NoneType
            (list, list),
            (list, List),
            (dict, dict),
            (dict, Dict),
            (Dict[str, str], Dict[Any, Any]),
            (Dict[str, int], Dict[str, int]),
            (str, Union[str, Dict[str, Any]]),
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
            (Dict[str, int], Dict[str, str]),
            (int, Union[str, Dict[str, Any]]),
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

    def test_validation(self):
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
                ([], List),
                ({}, dict),
                ({}, Dict),

                # Typed containers
                (["item1", "item2"], List[str]),
                ([1, 2, 3], List[int]),
                ({"lorem": "ipsum"}, Dict[str, str]),
                ({"lorem": 123}, Dict[str, int]),
                ([TestClassA(), TestClassB()], List[TestClassA]),

                # Union and Optional
                (None, Optional[str]),
                ("hello", Union[str, int]),
                (123, Union[str, int]),
                ({"key": "value"}, Union[str, Dict[str, str]]),
                (None, Union[str, NoneType]),
                ("optional", Optional[str]),

                # Callable
                (_test_callable, Callable),
                (_test_callable, Callable[..., Any]),
                (_test_callable, Callable[..., bool]),

                # Tuples and Sets
                ((1, "str"), Tuple[int, str]),
                ({"apple", "banana"}, Set[str]),
                ({1, 2, 3}, Set[int]),

                # Nested types
                ({"nested": {"key": "value"}}, Dict[str, Dict[str, str]]),
                ([{"key": 1}, {"key": 2}], List[Dict[str, int]]),
                (({"key": "value"}, 123), Tuple[Dict[str, str], int]),

                # Classes and types
                (TestClassA(), TestClassA),
                (TestClassB(), TestClassA),  # Compatibility with superclass
                (TestClassB(), TestClassB),

                # Class types
                (TestClassA, Type[TestClassA]),
                (TestClassB, Type[TestClassA]),
                (TestClassB, Type[TestClassB]),
                (TestClassA, Type),
                (TestClassB, Type),

                # Nested Unions and Optionals
                ({"key": "value"}, Union[Dict[str, str], List[str]]),
                ([1, 2, 3], Union[List[int], Set[int]]),
                ({"key": "value"}, Union[Dict[str, str], NoneType]),
                (None, Union[Dict[str, str], NoneType]),
                (123, Union[Optional[int], NoneType]),
                (TestClassB(), Union[TestClassA, TestClassB]),
                (TestClassB(), Union[TestClassA, str]),
                (TestClassB, Union[Type[TestClassA], Type[TestClassB]]),
            ],
            failure_cases=[
                # Type mismatches
                (123, str),
                ("123", int),
                (None, int),

                # Container type mismatches
                ({}, list),
                ([], dict),
                ({"lorem": 123}, Dict[str, str]),

                # Union mismatches
                (123, Union[str, Dict[str, Any]]),
                ("not_callable", Callable[..., str]),

                # Callable with incompatible signature
                (_test_callable, Callable[..., str]),

                # Class type mismatches
                (TestClassA(), TestClassB),  # TestClassA instance is not compatible with TestClassB type
                (123, TestClassA),
                ("str", TestClassB),

                # Type mismatches for class types
                (TestClassA(), Type[TestClassA]),  # TestClassA() is an instance, not a type
                (TestClassB(), Type),

                # Non-type values for Type
                (123, Type),
                ("str", Type),

                # Incorrect nested types
                ([1, "str"], List[int]),
                ({"key": 123}, Dict[str, str]),
                ({"key": "value"}, List[Dict[str, str]]),  # Expecting List, got Dict
                (["str"], Set[str]),  # List vs. Set

                # Incorrect Optional and Union usage
                (123, Optional[str]),  # Expecting str or None
                (None, int),  # NoneType mismatch

                # Tuple and Set mismatches
                ((1, "str"), Tuple[str, int]),  # Type order mismatch in Tuple
                ({"apple", 1}, Set[str]),  # Mixed types in Set
                (TestClassA, Union[int, str, float]),
                (TestClassA, Union[TestClassB]),
                (TestClassA, TestClassB),
                (TestClassA, TestClassA),
            ]
        )
