from __future__ import annotations

from wexample_helpers.exception.undefined_exception import UndefinedException


class KeyNotFoundError(UndefinedException):
    """Exception raised when a key is not found in a list of available keys."""

    error_code: str = "KEY_NOT_FOUND"

    def __init__(
        self, message: str, key: str, available_keys: list[str], **kwargs
    ) -> None:
        """
        Initialize the exception with the missing key and available keys.

        :param key: The key that was not found
        :param available_keys: List of keys that are available
        """
        self.key = key
        self.available_keys = available_keys
        super().__init__(
            message=f"{message}: '{key}'. Available keys: {available_keys}",
            data={"key": key, "available_keys": available_keys},
            **kwargs,
        )
