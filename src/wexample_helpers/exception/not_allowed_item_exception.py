from __future__ import annotations

from typing import ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.exception.mixin.not_allowed_item_mixin import NotAllowedItemMixin
from wexample_helpers.exception.undefined_exception import UndefinedException


@base_class
class NotAllowedItemException(UndefinedException, NotAllowedItemMixin):
    """Base exception for cases where an item is not allowed or not provided.

    This exception should be used when:
    1. A specific item value is not in a list of allowed values
    2. A required item was not provided at all
    """

    error_code: ClassVar[str] = "NOT_ALLOWED_ITEM"

    item_type: str = public_field(description="Type of the offending item")
    item_value: str | None = public_field(
        default=None, description="Value of the item that is not allowed"
    )
    allowed_values: list[str] = public_field(
        factory=list, description="List of allowed values for this item type"
    )

    def _build_message(self) -> str:
        return self.format_not_allowed_item_message(
            item_type=self.item_type,
            item_value=self.item_value,
            allowed_values=self.allowed_values,
        )
