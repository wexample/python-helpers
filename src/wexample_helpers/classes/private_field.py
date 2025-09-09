from typing import Callable, Any

from wexample_helpers.classes.base_field import BaseField
from wexample_helpers.enums.field_visibility import FieldVisibility


class PrivateField(BaseField):
    """Private field - must start with underscore."""

    @property
    def visibility(self) -> FieldVisibility:
        return FieldVisibility.PRIVATE

def private_field(description: str, validator: Callable = None, **kwargs) -> Any:
    """Create a private field."""
    return PrivateField(description, validator, **kwargs).to_attrs_field()