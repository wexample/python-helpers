from __future__ import annotations

from wexample_helpers.exception.not_allowed_item_exception import (
    NotAllowedItemException,
)


class CommandUnexpectedArgumentException(NotAllowedItemException):
    """Exception raised when an unexpected argument is provided to a command."""

    error_code: str = "COMMAND_UNEXPECTED_ARGUMENT"

    def __init__(
        self,
        argument: str,
        allowed_arguments: list[str],
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        super().__init__(
            item_type="argument",
            item_value=argument,
            allowed_values=allowed_arguments,
            cause=cause,
            previous=previous,
        )
