from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers.const.types import StringKeysDict


class SerializableMixin:
    def hydrate(self, data: StringKeysDict) -> None:
        pass

    def serialize(self) -> StringKeysDict:
        return {}
