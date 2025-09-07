from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type

import attrs

from .attrs_circular_service import Service

if TYPE_CHECKING:
    pass


@attrs.define(eq=False)
class BaseKernel:
    """Base kernel using attrs; creates its Service and initializes circular link."""

    name: str
    debug: bool = False
    _service: Service | None = attrs.field(default=None, eq=False)

    def __attrs_post_init__(self) -> None:
        service_cls = self.get_service_class()
        self._service = service_cls(name=f"{self.name}_service")
        self._service.initialize(self)

    @property
    def service(self) -> Service:
        assert self._service is not None
        return self._service

    @classmethod
    def get_service_class(cls) -> type[Service]:
        return Service
