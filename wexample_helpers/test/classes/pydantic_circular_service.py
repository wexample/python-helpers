from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, Field, PrivateAttr

if TYPE_CHECKING:
    from .pydantic_circular_kernel import Kernel


class Service(BaseModel):
    """A service that needs access to its parent kernel."""

    name: str = Field(description="Service name")
    enabled: bool = Field(default=True)

    # Private reference to parent
    _kernel: Optional["Kernel"] = PrivateAttr(default=None)

    def initialize(self, kernel: "Kernel") -> None:
        """Initialize the service with its parent kernel."""
        self._kernel = kernel

    @property
    def kernel(self) -> Optional["Kernel"]:
        """Get the parent kernel."""
        return self._kernel
