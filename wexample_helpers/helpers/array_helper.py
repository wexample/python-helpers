from typing import List, Any


def array_swap(two_items_array: List[Any], do_swap: bool) -> List[Any]:
    if do_swap:
        two_items_array.reverse()

        return two_items_array

    return two_items_array
