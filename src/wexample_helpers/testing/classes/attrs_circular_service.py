from __future__ import annotations

from typing import TYPE_CHECKING

from ...classes.field import public_field
from ...decorator.base_class import base_class

if TYPE_CHECKING:
    from .attrs_circular_base_kernel import AdvancedKernel, BaseKernel


@base_class
class Service:
    # Backlink to the owning kernel: excluded from equality, otherwise the
    # attrs generated __eq__ recurses forever (kernel -> service -> kernel).
    kernel: BaseKernel | None = public_field(
        default=None,
        description="Owning kernel this service is attached to",
        eq=False,
    )
    name: str

    @property
    def advanced_kernel(self) -> AdvancedKernel | None:
        # Only available when attached to an AdvancedKernel
        k = self.kernel
        if k is not None and type(k).__name__ == "AdvancedKernel":
            # Avoid direct import to keep circular hints safe at runtime
            return k  # type: ignore[return-value]
        return None

    @property
    def base_kernel(self) -> BaseKernel | None:
        return self.kernel

    @property
    def mode(self) -> str:
        return "basic"

    def initialize(self, kernel: BaseKernel) -> None:
        self.kernel = kernel


@base_class
class AdvancedService(Service):
    @property
    def mode(self) -> str:
        return "advanced"
