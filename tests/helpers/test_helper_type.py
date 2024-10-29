from typing import Any, List, Dict, Tuple, Union

from wexample_helpers.helpers.type_helper import type_is_generic


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
