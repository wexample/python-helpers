from collections.abc import Callable
from typing import Any

import attrs
from wexample_helpers.classes.base_field import BaseField
from wexample_helpers.enums.field_visibility import FieldVisibility


def public_field(
        description: str,
        validator: None | Callable | list[Callable] = None,
        default: Any = attrs.NOTHING,
        **kwargs
) -> Any:
    """Create a public field."""
    return Field(description, validator=validator, default=default, **kwargs).to_attrs_field()


class Field(BaseField):
    """Standard public field."""

    @property
    def visibility(self) -> FieldVisibility:
        return FieldVisibility.PUBLIC
