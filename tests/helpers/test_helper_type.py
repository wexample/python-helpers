from types import NoneType
from typing import Any, Callable, Dict, List, Tuple, Union, Type

import pytest
from wexample_helpers.helpers.type_helper import (
    type_is_compatible,
    type_is_generic,
    type_validate_or_fail,
)


class TestHelperType:
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

        success_cases = [
            ("str", Any),
            (True, Any),
            ("str", str),
            (123, int),
            (123.123, float),
            (None, NoneType),
            ([], list),
            ([], List),
            ({}, dict),
            ({}, Dict),
            ({"lorem": "ipsum"}, Dict[str, str]),
            ({"lorem": 123}, Dict[str, int]),
            ({}, Union[str, Dict[str, Any]]),
            (_test_callable, Callable),
            (_test_callable, Callable[..., Any]),
            (_test_callable, Callable[..., bool]),
            (TestClassA(), TestClassA),
            (TestClassB(), TestClassA),
            (TestClassB(), TestClassB),
            (TestClassA, Type[TestClassA]),
            (TestClassB, Type[TestClassA]),
            (TestClassB, Type[TestClassB]),
            (TestClassA, Type),
            (TestClassB, Type),
        ]

        failure_cases = [
            (123, str),
            ("123", int),
            (None, int),
            ({}, list),
            ([], dict),
            ({"lorem": 123}, Dict[str, str]),
            (123, Union[str, Dict[str, Any]]),
            (_test_callable, Callable[..., str]),
            (TestClassA(), TestClassB),
            (123, TestClassA),
            ("str", TestClassB),
            (TestClassA(), Type[TestClassA]),
            (TestClassB(), Type),
            (123, Type),
            ("str", Type),
        ]

        # Success cases: should not raise exceptions
        for value, expected_type in success_cases:
            type_validate_or_fail(
                value=value,
                allowed_type=expected_type,
            )

        # Failure cases: should raise InvalidOptionValueTypeException
        for value, expected_type in failure_cases:
            with pytest.raises(TypeError):
                type_validate_or_fail(
                    value=value,
                    allowed_type=expected_type,
                )
