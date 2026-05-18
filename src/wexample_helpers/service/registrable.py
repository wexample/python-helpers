from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Registrable(Protocol):
    """Protocol for items that can be stored in a Registry.

    Items expose their own key (no external assignment), declare their
    dependencies on other Registrable types, and provide sync/async init
    hooks so the Registry can drive their lifecycle uniformly.
    """

    @classmethod
    def get_registry_key(cls) -> str:
        """Unique key under which this item is stored in the registry."""
        ...

    @classmethod
    def dependencies(cls) -> list[type[Registrable]]:
        """Other Registrable types that must be initialized before this one.

        Used by Registry.resolve_init_order() for topological sorting.
        Return [] when there is no dependency.
        """
        ...

    def init_sync(self) -> None:
        """Synchronous initialization hook. Called by Registry.init_all_sync()."""
        ...

    async def init_async(self) -> None:
        """Asynchronous initialization hook. Called by Registry.init_all_async().

        Default implementation should call init_sync() in a thread (asyncio.to_thread)
        unless the item has a genuinely async init path (network, asyncio-native I/O).
        """
        ...
