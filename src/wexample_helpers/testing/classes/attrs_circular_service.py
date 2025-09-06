from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import attrs

if TYPE_CHECKING:
    from .attrs_circular_base_kernel import BaseKernel, AdvancedKernel


@attrs.define(eq=False)
class Service:
    name: str
    kernel: Optional[BaseKernel] = None

    def initialize(self, kernel: BaseKernel) -> None:
        self.kernel = kernel

    @property
    def mode(self) -> str:
        return "basic"

    @property
    def base_kernel(self) -> Optional[BaseKernel]:
        return self.kernel

    @property
    def advanced_kernel(self) -> Optional[AdvancedKernel]:
        # Only available when attached to an AdvancedKernel
        k = self.kernel
        if k is not None and k.__class__.__name__ == "AdvancedKernel":
            # Avoid direct import to keep circular hints safe at runtime
            return k  # type: ignore[return-value]
        return None


@attrs.define(eq=False)
class AdvancedService(Service):
    @property
    def mode(self) -> str:
        return "advanced"
