from __future__ import annotations

from typing import TypedDict


class NotAllowedItemData(TypedDict):
    """Data structure for exceptions related to not allowed items."""

    item_type: str
    item_value: str | None
    allowed_values: list[str]
    is_missing: bool
