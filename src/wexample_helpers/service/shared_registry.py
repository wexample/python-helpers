from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.service.registry import Registry

if TYPE_CHECKING:
    from typing import Self

T = TypeVar("T")


@base_class
class SharedRegistry(Registry[T]):
    """Registry exposing a per-class shared instance via shared().

    Cooperative `__init__` (forwards through MRO via super()) so this class
    can be combined with other Registry variants (e.g. DiskPersistedRegistry)
    via multiple inheritance without dropping kwargs.

    Use this when a registry is meant to be globally accessible without
    threading an instance reference through call sites. Each subclass gets
    its own shared instance (the cache key is the concrete class, not
    SharedRegistry itself), so distinct subclasses do not collide.

        class MyRegistry(SharedRegistry[MyType]):
            ...

        MyRegistry.shared().register(item, key="foo")
        item = MyRegistry.shared().get("foo")

    Instantiation as a regular Registry is still supported for cases where
    a dedicated, non-shared instance is needed:

        local = MyRegistry()
        local.register(item)
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def reset_shared(cls) -> None:
        """Drop the per-class shared instance (useful for tests)."""
        if "_shared_instance" in cls.__dict__:
            delattr(cls, "_shared_instance")

    @classmethod
    def shared(cls) -> Self:
        """Return the per-class shared instance, lazily created on first call."""
        if "_shared_instance" not in cls.__dict__:
            cls._shared_instance = cls()
        return cls._shared_instance
