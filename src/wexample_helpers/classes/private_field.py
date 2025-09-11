from typing import Any, Callable

from wexample_helpers.classes.base_field import BaseField
from wexample_helpers.enums.field_visibility import FieldVisibility


def private_field(description: str, validator: Callable = None, init: bool = False, **kwargs) -> Any:
    """Create a private field. Private fields have init=False by default."""
    return PrivateField(description, validator, init=init, **kwargs).to_attrs_field()


class PrivateField(BaseField):
    """Private field - must start with underscore."""

    @property
    def visibility(self) -> FieldVisibility:
        return FieldVisibility.PRIVATE