from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .attrs_circular_service import Service

if TYPE_CHECKING:
    pass


@attrs.define(eq=False)
class BaseKernel:
    """Base kernel using attrs; creates its Service and initializes circular link."""

    debug: bool = False

    name: str
    _service: Service | None = attrs.field(default=None, eq=False)

    def __attrs_post_init__(self) -> None:
        service_cls = self.get_service_class()
        self._service = service_cls(name=f"{self.name}_service")
        self._service.initialize(self)

    @classmethod
    def get_service_class(cls) -> type[Service]:
        return Service

    @property
    def service(self) -> Service:
        assert self._service is not None
        return self._service
