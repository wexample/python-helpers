from __future__ import annotations

from typing import Any, TypeVar

from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.service.registry import Registry

T = TypeVar("T")


@base_class
class SingletonRegistry(Registry[T]):
    """Registry of classes maintained as singleton instances.

    register(cls) stores the class. After init_all_sync() or init_all_async(),
    one instance per class is created and accessible via get(key). Topological
    order is honored via the Registrable.dependencies() classmethod when present.
    """

    _classes: dict[str, type[T]] | None = private_field(
        factory=dict, description="Registered classes (instantiated on init_all_*)"
    )

    def __init__(self, container: Any = None) -> None:
        super().__init__(container=container)
        self._classes = {}

    @staticmethod
    def _get_deps(cls: Any) -> list[type]:
        deps_fn = getattr(cls, "dependencies", None)
        if deps_fn is not None:
            return deps_fn() or []
        return []

    def get_all_classes(self) -> dict[str, type[T]]:
        return self._classes

    def get_class(self, key: str) -> type[T] | None:
        return self._classes.get(key)

    async def init_all_async(self) -> None:
        """Instantiate by topological layers; gather init_async within each layer."""
        import asyncio

        for layer in self._resolve_layers():
            instances = []
            for cls in layer:
                instance = self._instantiate(cls)
                self._items[self._derive_key(cls)] = instance
                instances.append(instance)
            coros = [
                m() for inst in instances
                if (m := getattr(inst, "init_async", None)) is not None
            ]
            if coros:
                await asyncio.gather(*coros)

    def init_all_sync(self) -> None:
        """Instantiate all classes in topological order, calling init_sync()."""
        for cls in self._resolve_order():
            instance = self._instantiate(cls)
            self._items[self._derive_key(cls)] = instance
            init_sync = getattr(instance, "init_sync", None)
            if init_sync is not None:
                init_sync()

    def register(self, item: type[T], key: str | None = None) -> None:
        """Register a class. Instance is created during init_all_*()."""
        if not isinstance(item, type):
            raise TypeError(
                f"SingletonRegistry only accepts classes, got instance of {type(item).__name__}"
            )
        if key is None:
            key = self._derive_key(item)
        self._classes[key] = item

    def _instantiate(self, cls: type[T]) -> T:
        try:
            return cls(container=self.container)
        except TypeError:
            return cls()

    def _resolve_layers(self) -> list[list[type[T]]]:
        """Layered topological order: each layer can be initialized in parallel."""
        classes = self._classes
        derive_key = self._derive_key
        depth: dict[str, int] = {}

        def compute(cls: type[T]) -> int:
            key = derive_key(cls)
            if key in depth:
                return depth[key]
            d = 0
            for dep in self._get_deps(cls):
                dep_key = derive_key(dep)
                if dep_key in classes:
                    d = max(d, compute(classes[dep_key]) + 1)
            depth[key] = d
            return d

        for cls in classes.values():
            compute(cls)

        layers: dict[int, list[type[T]]] = {}
        for cls in classes.values():
            layers.setdefault(depth[derive_key(cls)], []).append(cls)
        return [layers[d] for d in sorted(layers)]

    def _resolve_order(self) -> list[type[T]]:
        """Flat topological sort: each class appears after its dependencies."""
        classes = self._classes
        derive_key = self._derive_key
        ordered: list[type[T]] = []
        visited: set[str] = set()
        visiting: set[str] = set()

        def visit(cls: type[T]) -> None:
            key = derive_key(cls)
            if key in visited:
                return
            if key in visiting:
                chain = " -> ".join([*visiting, key])
                raise ValueError(f"Cyclic dependency detected: {chain}")
            visiting.add(key)
            for dep in self._get_deps(cls):
                dep_key = derive_key(dep)
                if dep_key in classes:
                    visit(classes[dep_key])
            visiting.discard(key)
            visited.add(key)
            ordered.append(cls)

        for cls in classes.values():
            visit(cls)
        return ordered
