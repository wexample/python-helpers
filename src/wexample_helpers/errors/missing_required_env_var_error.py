from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.exception.undefined_exception import UndefinedException

if TYPE_CHECKING:
    from wexample_helpers.const.types import StringsList


@base_class
class MissingRequiredEnvVarError(UndefinedException):
    """Custom exception raised when required environment variables are missing."""

    error_code: ClassVar[str] = "MISSING_REQUIRED_ENV_VAR"

    missing_keys: StringsList = public_field(
        description="Names of the missing required environment variables"
    )

    def _build_message(self) -> str:
        return f"Missing required environment variables: {', '.join(self.missing_keys)}"
