from __future__ import annotations

from typing import Any

from wexample_helpers.exception.undefined_exception import UndefinedException


class MultipleBaseModelInheritanceError(UndefinedException):
    """Exception raised when multiple inheritance of BaseModel is detected."""

    error_code: str = "MULTIPLE_BASE_MODEL_INHERITANCE"

    def __init__(self, class_instance: Any, **kwargs) -> None:
        super().__init__(
            message=(
                f"Multiple inheritance of BaseModel is not allowed in class "
                f"'{class_instance.__name__}'."
            ),
            **kwargs,
        )
