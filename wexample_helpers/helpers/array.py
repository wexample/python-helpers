from typing import Any, List, Sequence


def array_replace_value(
    array: Sequence[Any], search: Any, replacement: Any
) -> List[Any]:
    return [replacement if value == search else value for value in array]


def array_swap(two_items_array: List[Any], do_swap: bool) -> List[Any]:
    if do_swap:
        two_items_array.reverse()

        return two_items_array

    return two_items_array


def array_unique(array: Sequence[Any]) -> List[Any]:
    return list(set(array))
