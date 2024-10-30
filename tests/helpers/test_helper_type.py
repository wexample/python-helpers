from typing import Any, Dict, List, Union, Callable, Tuple

from wexample_helpers.helpers.type_helper import type_is_generic, type_is_compatible


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
            assert type_is_generic(type_), f"{type_} should be detected as a generic type"

        for type_ in should_not_be_true:
            assert not type_is_generic(type_), f"{type_} should NOT be detected as a generic type"

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
            (Callable[..., bool], Callable[..., str])
        ]

        for actual_type, expected_type in success_cases:
            assert type_is_compatible(actual_type,
                                      expected_type), f"Expected {actual_type} to be compatible with {expected_type}"

        for actual_type, expected_type in failure_cases:
            assert not type_is_compatible(actual_type,
                                          expected_type), f"Expected {actual_type} to be incompatible with {expected_type}"
