from __future__ import annotations

from wexample_helpers.exception.undefined_exception import UndefinedException


class GatewayError(UndefinedException):
    """Base exception for gateway errors."""

    error_code: str = "GATEWAY_ERROR"

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message=message, **kwargs)
