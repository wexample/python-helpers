from __future__ import annotations

from typing import Any, ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.exception.not_allowed_item_exception import (
    NotAllowedItemException,
)
from wexample_helpers.helpers.string import string_truncate
from wexample_helpers.helpers.type import type_to_name


@base_class
class NotAllowedVariableTypeException(NotAllowedItemException):
    """A specific exception for bad variables types"""

    error_code: ClassVar[str] = "NOT_ALLOWED_VARIABLE_TYPE"

    variable_type: Any = public_field(description="Type of the offending variable")
    variable_value: Any = public_field(description="Value of the offending variable")
    allowed_types: list[Any] = public_field(
        factory=list, description="List of allowed types for the variable"
    )
    item_type: str = public_field(
        default="type", description="Type of the offending item"
    )

    def _build_message(self) -> str:
        types_str = (
            ", ".join(type_to_name(t) for t in self.allowed_types)
            if self.allowed_types
            else "<none>"
        )
        return (
            f"Invalid variable type '{type_to_name(self.variable_type)}' for value "
            f"{string_truncate(str(self.variable_value), 1000)!r}. "
            f"Allowed types: {types_str}."
        )
