from typing import Type, TypeVar

from wexample_helpers.const.types import StringKeysDict

T = TypeVar("T", bound="SerializableMixin")


class SerializableMixin:
    def to_dict(self) -> StringKeysDict:
        return {}

    def _hydrate(self, data: StringKeysDict) -> None:
        return None

    @classmethod
    def from_dict(cls: Type[T], data: StringKeysDict) -> T:
        instance = cls()
        instance._hydrate(data)

        return instance
