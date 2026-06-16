from __future__ import annotations

from typing import Any, Generic, TypeVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

T = TypeVar("T")


@base_class
class Registry(Generic[T]):
    """Generic key/value registry for typed items.

    The base Registry is tolerant: it accepts both classes and instances,
    derives keys automatically when possible, and does not manage item
    lifecycle. Use SingletonRegistry for auto-instantiation + init hooks.
    For disk-backed state see DiskPersistedRegistry in wexample_filestate
    (lives in filestate because it requires a StructuredContentFile).
    """

    container: Any = public_field(
        default=None, description="Optional container reference"
    )
    _fail_if_missing: bool = private_field(
        default=False, description="Raise KeyError when a missing item is fetched"
    )
    _items: dict[str, T] | None = private_field(
        factory=dict, description="The items of the registry"
    )

    def __init__(self, container: Any = None) -> None:
        # Custom __init__ bypasses attrs' auto-init, so we must seed every
        # field declared via private_field/public_field with its default.
        self._items = {}
        self._fail_if_missing = False
        self.container = container

    @staticmethod
    def _derive_key(item: Any) -> str:
        # getattr-with-sentinel avoids the double attribute lookup that
        # hasattr() + subsequent access would incur.
        method = getattr(item, "get_registry_key", None)
        if method is not None:
            return method()
        method = getattr(item, "get_snake_short_class_name", None)
        if method is not None:
            return method()
        if isinstance(item, type):
            return item.__name__
        return type(item).__name__

    def all_keys(self) -> list[str]:
        return list(self._items.keys())

    def get(self, key: str) -> T | None:
        item = self._items.get(key)
        self._raise_error_if_expected(key, item)
        return item

    def get_all(self) -> dict[str, T]:
        return self._items

    def has(self, key: str) -> bool:
        return key in self._items

    def register(self, item: T, key: str | None = None) -> None:
        """Register an item. Key is auto-derived if not provided.

        Auto-derivation order:
        1. item.get_registry_key() (Registrable Protocol)
        2. item.get_snake_short_class_name() (existing wexample classes)
        3. item.__name__ (raw classes)
        4. type(item).__name__ (raw instances)
        """
        if key is None:
            key = self._derive_key(item)
        self._items[key] = item

    def register_many(self, items: list[T]) -> None:
        for item in items:
            self.register(item)

    def _raise_error_if_expected(self, key: str, item: Any) -> None:
        # Check the flag first: it is False by default, so the common path
        # short-circuits immediately without evaluating `item is None`.
        if self._fail_if_missing and item is None:
            raise KeyError(
                f"Item not found in registry: {key}. Available keys: {self.all_keys()}"
            )
