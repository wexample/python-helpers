from typing import Type, Dict, TypeVar, Any

from wexample_helpers.const.types import StringKeysDict

T = TypeVar("T", bound="SerializableMixin")


class SerializableMixin:
    def to_dict(self) -> StringKeysDict:
        return {}

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        return cls(**data)
