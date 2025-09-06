from __future__ import annotations

from pydantic import Field
from .pydantic_circular_base_kernel import BaseKernel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pydantic_circular_advanced_service import AdvancedService


class AdvancedKernel(BaseKernel):
    """Advanced kernel with additional features."""

    version: str = Field(default="1.0.0")
    features: list[str] = Field(default_factory=list)

    @classmethod
    def get_service_class(cls) -> type[AdvancedService]:
        """Override to use AdvancedService."""
        from pydantic_circular_advanced_service import AdvancedService
        return AdvancedService
