from __future__ import annotations

# datetime is used at runtime (field factory), not only in annotations.
from datetime import datetime
from typing import Any

from ...classes.base_class import BaseClass
from ...classes.private_field import private_field
from ...decorator.base_class import base_class


@base_class
class PrivateFieldsMixin(BaseClass):
    """Mixin providing private attributes template.

    State is declared with private_field on an attrs mixin (same pattern as
    WithPathMixin): a plain __init__ would never run, since the attrs
    generated __init__ of the consuming class does not chain to it.
    """

    _created_at: datetime = private_field(
        factory=datetime.now,
        description="Timestamp when the object was created",
    )
    _metadata: dict[str, Any] = private_field(
        factory=dict,
        description="Internal metadata storage",
    )
    _secret_key: str = private_field(
        default="default-key",
        description="Internal secret key",
    )

    @property
    def created_at(self) -> datetime:
        """Read-only access to creation time."""
        return self._created_at

    def get_metadata(self) -> dict[str, Any]:
        """Safe access to private metadata."""
        return self._metadata.copy()

    def set_metadata(self, key: str, value: Any) -> None:
        """Safely set metadata value."""
        self._metadata[key] = value
