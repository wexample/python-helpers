from __future__ import annotations

from wexample_helpers.exception.undefined_exception import ExceptionData


class NotAllowedItemData(ExceptionData):
    """Data model for exceptions related to not allowed items."""

    # NOTE: We intentionally avoid Pydantic here. Provide a simple
    # initializer and a `model_dump()` method to keep compatibility with
    # existing call sites that previously relied on Pydantic models.
    def __init__(
        self,
        item_type: str,
        item_value: str | None = None,
        allowed_values: list[str] | None = None,
        is_missing: bool = False,
    ) -> None:
        self.item_type = item_type
        self.item_value = item_value
        self.allowed_values = allowed_values or []
        self.is_missing = is_missing

    def model_dump(self) -> dict:
        """Return a dict representation similar to Pydantic's model_dump()."""
        return {
            "item_type": self.item_type,
            "item_value": self.item_value,
            "allowed_values": list(self.allowed_values),
            "is_missing": self.is_missing,
        }
