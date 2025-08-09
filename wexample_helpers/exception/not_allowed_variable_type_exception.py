from typing import List, Optional, Type, Any

from mypy.types import UnionType

from wexample_helpers.exception.not_allowed_item_exception import NotAllowedItemException


class NotAllowedVariableTypeException(NotAllowedItemException):
    """A specific exception for bad variables types"""
    error_code: str = "NOT_ALLOWED_VARIABLE_TYPE"

    def __init__(
            self,
            variable_type: str,
            variable_value: Any,
            allowed_types: List[Type | UnionType] = None,
            cause: Optional[Exception] = None,
            previous: Optional[Exception] = None
    ):
        from helper.string import string_truncate
        types_str = "', '".join(allowed_types)

        super().__init__(
            item_type='type',
            item_value=variable_type,
            allowed_values=allowed_types,
            cause=cause,
            previous=previous,
            message=f"Unexpected variable of type {variable_type} (value: \"{string_truncate(variable_value, 40)}\"). Allowed types are {types_str}"
        )
