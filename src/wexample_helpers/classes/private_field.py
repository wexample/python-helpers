from typing import Callable, Any

from wexample_helpers.classes.base_field import BaseField
from wexample_helpers.enums.field_visibility import FieldVisibility


class PrivateField(BaseField):
    """Private field - must start with underscore."""

    @property
    def visibility(self) -> FieldVisibility:
        return FieldVisibility.PRIVATE

def private_field(description: str, validator: Callable = None, init: bool = False, **kwargs) -> Any:
    """Create a private field. Private fields have init=False by default."""
    return PrivateField(description, validator, init=init, **kwargs).to_attrs_field()