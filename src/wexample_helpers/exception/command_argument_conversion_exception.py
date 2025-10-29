from __future__ import annotations

from typing import TypedDict

from wexample_helpers.exception.undefined_exception import UndefinedException


class CommandArgumentConversionData(TypedDict):
    """Data structure for CommandArgumentConversion exception."""

    argument_name: str
    target_type: str
    value: str


class CommandArgumentConversionException(UndefinedException):
    """Exception raised when a command argument cannot be converted to the expected type."""

    error_code: str = "COMMAND_ARGUMENT_CONVERSION_ERROR"

    def __init__(
        self,
        argument_name: str,
        value: str,
        target_type: type,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        data: CommandArgumentConversionData = {
            "argument_name": argument_name,
            "value": value,
            "target_type": target_type.__name__,
        }

        super().__init__(
            message=f"Cannot convert value '{value}' for argument '{argument_name}' to type {target_type.__name__}",
            data=data,
            cause=cause,
            previous=previous,
        )
