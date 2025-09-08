from __future__ import annotations

from datetime import datetime
from typing import Any


class PrivateFieldsMixin:
    """Mixin providing private attributes template."""
    _created_at: datetime

    _metadata: dict[str, Any]
    _secret_key: str = "default-key"

    def __init__(self) -> None:
        self._created_at = datetime.now()
        self._metadata = {}

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
