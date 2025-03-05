from datetime import datetime
from typing import Dict, Any

from pydantic import PrivateAttr


class PydanticPrivateMixin:
    """Mixin providing private Pydantic attributes without inheriting from BaseModel."""

    _created_at: datetime = PrivateAttr(default_factory=datetime.now)
    _metadata: Dict[str, Any] = PrivateAttr(default_factory=dict)
    _secret_key: str = PrivateAttr(default="default-key")

    def get_metadata(self) -> Dict[str, Any]:
        """Safe access to private metadata."""
        return self._metadata.copy()

    def set_metadata(self, key: str, value: Any) -> None:
        """Safely set metadata value."""
        self._metadata[key] = value

    @property
    def created_at(self) -> datetime:
        """Read-only access to creation time."""
        return self._created_at
