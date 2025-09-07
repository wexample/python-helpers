from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum

import attrs
from attrs.validators import ge, le


class Status(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    INACTIVE = "inactive"


@attrs.define
class AttrsAdvanced:
    """An attrs-based equivalent of the former PydanticAdvanced."""

    # Public fields
    id: str
    status: Status = Status.PENDING

    # Complex types
    metadata: dict[str, str | int | bool] = attrs.field(factory=dict)

    # Score with range enforcement and rounding
    score: float = attrs.field(
        default=0.0,
        converter=lambda v: round(float(v), 2),
        validator=[ge(0), le(100)],
    )

    # Private-like internal state
    _secret_key: str = attrs.field(default="private")
    _created_at: datetime = attrs.field(factory=datetime.now)
    _internal_notes: list[str] = attrs.field(factory=list)

    # Note: range validation is handled by attrs validators and rounding by the converter above.

    @property
    def age(self) -> timedelta:
        return datetime.now() - self._created_at

    @property
    def is_active(self) -> bool:
        return self.status == Status.ACTIVE

    @property
    def notes(self) -> list[str]:
        return list(self._internal_notes)

    @notes.setter
    def notes(self, value: list[str]) -> None:
        self._internal_notes = [note.strip() for note in value]
