from datetime import datetime
from typing import Dict, Any


class PydanticPrivateMixin:
    """Mixin providing private attributes template for Pydantic classes."""

    def __init__(self):
        self._created_at = datetime.now()
        self._metadata = {}
        self._secret_key = "default-key"

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
