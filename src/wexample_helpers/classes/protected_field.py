from typing import Any
from collections.abc import Callable

from wexample_helpers.classes.base_field import BaseField
from wexample_helpers.enums.field_visibility import FieldVisibility


def protected_field(description: str, validator: Callable = None, **kwargs) -> Any:
    """Create a protected field."""
    return ProtectedField(description, validator, **kwargs).to_attrs_field()


class ProtectedField(BaseField):
    """Protected field - must start with underscore."""

    @property
    def visibility(self) -> FieldVisibility:
        return FieldVisibility.PROTECTED