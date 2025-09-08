from __future__ import annotations

from datetime import datetime

import attrs


@attrs.define
class AttrsClass:
    """An attrs-based class with various field types.

    Mirrors the structure of PydanticClass for testing cattrs/attrs flows.
    """

    count: int = 0

    # Required fields
    name: str

    # Optional fields
    description: str | None = None
    tags: list[str] = attrs.field(factory=list)

    # Field with default factory
    created_at: datetime = attrs.field(factory=datetime.now)
