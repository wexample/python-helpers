from __future__ import annotations

import attrs

from ..mixins.private_fields_mixin import PrivateFieldsMixin
from ..mixins.public_fields_mixin import PublicFieldsMixin


@attrs.define
class AttrsInheritanceModel(PublicFieldsMixin, PrivateFieldsMixin):
    """attrs model combining both mixins with additional functionality."""
    description: str | None = None
    # Extra fields akin to the Pydantic version
    enabled: bool = True
    # PublicFieldsMixin expects these attributes to exist; define them with defaults
    name: str = ""
    priority: int = 0
    tags: list[str] = attrs.field(factory=list)
    version: str = "1.0.0"

    def __attrs_post_init__(self) -> None:
        # Initialize mixins that set private fields
        PrivateFieldsMixin.__init__(self)
        PublicFieldsMixin.__init__(self)
        # Initialize any mixin-specific stuff if needed
        self._metadata["initialized_at"] = self._created_at
