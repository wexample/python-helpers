from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.exception.undefined_exception import UndefinedException

if TYPE_CHECKING:
    from wexample_helpers.const.types import StringsList


class MissingRequiredEnvVarError(UndefinedException):
    """Custom exception raised when required environment variables are missing."""

    error_code: str = "MISSING_REQUIRED_ENV_VAR"

    def __init__(self, missing_keys: StringsList, **kwargs) -> None:
        self.missing_keys = missing_keys
        super().__init__(
            message=f"Missing required environment variables: {', '.join(missing_keys)}",
            data={"missing_keys": list(missing_keys)},
            **kwargs,
        )
