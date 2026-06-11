from __future__ import annotations

from typing import Any, ClassVar

from attrs import Factory

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.exception.undefined_exception import UndefinedException


@base_class
class MultipleBaseModelInheritanceError(UndefinedException):
    """Exception raised when multiple inheritance of BaseModel is detected."""

    class_instance: Any = public_field(
        description="Class for which multiple BaseModel inheritance was detected"
    )
    error_code: ClassVar[str] = "MULTIPLE_BASE_MODEL_INHERITANCE"
    message: str = public_field(
        default=Factory(
            lambda self: (
                f"Multiple inheritance of BaseModel is not allowed in class "
                f"'{self.class_instance.__name__}'."
            ),
            takes_self=True,
        ),
        description="Human-readable error message",
    )
