from __future__ import annotations

from wexample_helpers.exception.undefined_exception import UndefinedException


class GatewayError(UndefinedException):
    """Base exception for gateway errors.

    Kept with an explicit ``__init__`` (instead of the attrs ``@base_class``
    pattern) because it is constructed positionally as ``GatewayError("msg")``
    across the gateway code, which the kw-only attrs constructor forbids.
    """

    error_code: str = "GATEWAY_ERROR"

    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message=message, **kwargs)
