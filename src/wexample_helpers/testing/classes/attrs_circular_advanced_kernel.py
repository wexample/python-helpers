from __future__ import annotations

from .attrs_circular_base_kernel import BaseKernel
from .attrs_circular_service import AdvancedService, Service
from ...decorator.base_class import base_class


@base_class
class AdvancedKernel(BaseKernel):
    version: str = "1.0.0"

    @classmethod
    def get_service_class(cls) -> type[Service]:
        return AdvancedService
