from __future__ import annotations

from typing import Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.validator.abstract_validator import AbstractValidator


@base_class
class RangeValidator(AbstractValidator):
    max_value: int | float | None = public_field(
        default=None,
        description="Maximum allowed value (inclusive)",
    )
    min_value: int | float | None = public_field(
        default=None,
        description="Minimum allowed value (inclusive)",
    )

    def validate(self, value: Any) -> bool:
        """
        Validate that the value is within the specified range.

        Args:
            value: The value to validate (must be numeric)

        Returns:
            True if the value is within range, False otherwise
        """
        if not isinstance(value, (int, float)):
            return False

        min_value = self.min_value
        if min_value is not None and value < min_value:
            return False

        max_value = self.max_value
        if max_value is not None and value > max_value:
            return False

        return True

    def _get_default_error_message(self, value: Any) -> str:
        min_value = self.min_value
        max_value = self.max_value
        if min_value is not None and max_value is not None:
            return f"Value {value} must be between {min_value} and {max_value}"
        elif min_value is not None:
            return f"Value {value} must be at least {min_value}"
        elif max_value is not None:
            return f"Value {value} must be at most {max_value}"
        else:
            return f"Value {value} is invalid"
