from __future__ import annotations

import attrs

from .attrs_circular_base_kernel import BaseKernel
from .attrs_circular_service import AdvancedService, Service


@attrs.define(kw_only=True)
class AdvancedKernel(BaseKernel):
    version: str = "1.0.0"

    @classmethod
    def get_service_class(cls) -> type[Service]:
        return AdvancedService
