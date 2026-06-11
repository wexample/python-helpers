from __future__ import annotations

import uuid
from typing import Any, ClassVar

import attrs

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

# Base fields serialized explicitly by to_dict(); every other public field is
# considered domain-specific payload and merged into the "data" section.
_BASE_FIELD_NAMES = {
    "message",
    "data",
    "cause",
    "previous",
    "suggestions",
    "exception_id",
}


@base_class
class UndefinedException(Exception):
    """Base exception class for all application exceptions.

    Provides enhanced functionality including:
    - Unique error codes
    - Structured, serializable error data
    - Error chaining (cause/previous)
    - Resolution suggestions (human-actionable hints)
    - Serialization support
    """

    # Class-level error code, should be overridden by subclasses.
    error_code: ClassVar[str] = "UNDEFINED_ERROR"

    message: str = public_field(
        description="Human-readable error message",
    )
    data: dict[str, Any] = public_field(
        factory=dict,
        description="Structured, serializable error data",
    )
    cause: Exception | None = public_field(
        default=None,
        description="Underlying exception that triggered this error",
    )
    previous: Exception | None = public_field(
        default=None,
        description="Previous exception in the chain",
    )
    suggestions: list[str] = public_field(
        factory=list,
        description="Human-actionable hints to help resolve the error",
    )
    exception_id: str = public_field(
        init=False,
        factory=lambda: str(uuid.uuid4()),
        description="Unique identifier of this exception instance",
    )

    def __str__(self) -> str:
        # auto_exc stores every field in self.args, so rely on the message only.
        return self.message

    def collect_data(self) -> dict[str, Any]:
        """Return the structured payload: explicit ``data`` merged with every
        domain-specific public field declared by subclasses.

        This lets subclasses expose their context as plain ``public_field``s
        instead of hand-building a ``data={...}`` dict.
        """
        data = dict(self.data)
        for field in attrs.fields(type(self)):
            if field.name in _BASE_FIELD_NAMES or field.name.startswith("_"):
                continue
            data[field.name] = getattr(self, field.name)
        return data

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        data = self.collect_data()

        result: dict[str, Any] = {
            "error_code": self.error_code,
            "message": self.message,
            "exception_id": self.exception_id,
        }

        if data:
            result["data"] = data

        if self.suggestions:
            result["suggestions"] = self.suggestions

        if self.cause:
            result["cause"] = str(self.cause)

        return result

    def with_data(self, **kwargs) -> UndefinedException:
        """Add additional data to the exception."""
        self.data.update(kwargs)
        return self
