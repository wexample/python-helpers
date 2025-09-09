from typing import Callable, Any

from wexample_helpers.classes.base_field import BaseField
from wexample_helpers.enums.field_visibility import FieldVisibility


class Field(BaseField):
    """Standard public field."""

    @property
    def visibility(self) -> FieldVisibility:
        return FieldVisibility.PUBLIC

def public_field(description: str, validator: Callable = None, **kwargs) -> Any:
    """Create a public field."""
    return Field(description, validator, **kwargs).to_attrs_field()