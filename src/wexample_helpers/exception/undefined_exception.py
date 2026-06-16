from __future__ import annotations

import uuid
from typing import Any, ClassVar

import attrs

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

# Base fields serialized explicitly by to_dict(); every other public field is
# considered domain-specific payload and merged into the "data" section.
_BASE_FIELD_NAMES: frozenset[str] = frozenset({
    "message",
    "data",
    "cause",
    "previous",
    "suggestions",
    "exception_id",
})


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

    cause: Exception | None = public_field(
        default=None,
        description="Underlying exception that triggered this error",
    )
    data: dict[str, Any] = public_field(
        factory=dict,
        description="Structured, serializable error data",
    )
    # Class-level error code, should be overridden by subclasses.
    error_code: ClassVar[str] = "UNDEFINED_ERROR"
    exception_id: str = public_field(
        init=False,
        factory=lambda: str(uuid.uuid4()),
        description="Unique identifier of this exception instance",
    )
    message: str | None = public_field(
        default=None,
        description="Explicit error message; when omitted, _build_message() is used",
    )
    previous: Exception | None = public_field(
        default=None,
        description="Previous exception in the chain",
    )
    suggestions: list[str] = public_field(
        factory=list,
        description="Human-actionable hints to help resolve the error",
    )

    def __str__(self) -> str:
        # auto_exc stores every field in self.args, so rely on the message only.
        return self.render_message()

    def collect_data(self) -> dict[str, Any]:
        """Return the structured payload: explicit ``data`` merged with every
        domain-specific public field declared by subclasses.

        This lets subclasses expose their context as plain ``public_field``s
        instead of hand-building a ``data={...}`` dict.
        """
        data = {**self.data}
        for field in attrs.fields(type(self)):
            name = field.name
            if name in _BASE_FIELD_NAMES or name.startswith("_"):
                continue
            data[name] = getattr(self, name)
        return data

    def render_message(self) -> str:
        """Return the explicit message if provided, else the derived one.

        Computed lazily (not at init) so it never depends on attrs field
        declaration order — which the repo's field-sorting linter reshuffles.
        Always read the message through this, never ``self.message`` directly
        (which is None for subclasses that derive their message).
        """
        if self.message is not None:
            return self.message
        return self._build_message()

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        data = self.collect_data()

        result: dict[str, Any] = {
            "error_code": self.error_code,
            "message": self.render_message(),
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

    def _build_message(self) -> str:
        """Override in subclasses to derive the message from their fields."""
        return ""
