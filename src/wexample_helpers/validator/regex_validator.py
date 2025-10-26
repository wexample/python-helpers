from __future__ import annotations

import re
from typing import Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.validator.abstract_validator import AbstractValidator


@base_class
class RegexValidator(AbstractValidator):
    pattern: str = public_field(
        description="Regular expression pattern to match against",
    )
    flags: int = public_field(
        default=0,
        description="Regular expression flags (e.g., re.IGNORECASE)",
    )

    def __attrs_post_init__(self) -> None:
        self._compiled_pattern = re.compile(self.pattern, self.flags)

    def validate(self, value: Any) -> bool:
        """
        Validate that the value matches the regex pattern.

        Args:
            value: The value to validate (must be a string)

        Returns:
            True if the value matches the pattern, False otherwise
        """
        if not isinstance(value, str):
            return False

        return self._compiled_pattern.match(value) is not None

    def _get_default_error_message(self, value: Any) -> str:
        return f"Value '{value}' does not match pattern '{self.pattern}'"
