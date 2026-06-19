from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.helper.abstract_attempt_manager import (
    AbstractAttemptManager,
    AttemptOutcome,
)

T = TypeVar("T")


@base_class
class PollingCallbackManager(AbstractAttemptManager[T]):
    """Run a callback with poll-until-success semantics.

    The callback is invoked repeatedly; an attempt is considered successful
    when it returns a non-None value, or when `is_success_callback` (if set)
    returns True for the value. On exhaustion, a TimeoutError is raised with
    `timeout_message` (or a default).
    """

    callback: Callable[[], T | None] = public_field(
        description="Callable executed at each attempt; returns the value on success or None to keep polling."
    )
    is_success_callback: Callable[[object], bool] | None = public_field(
        description="Optional predicate to decide success from the callback's return value. Defaults to `value is not None`.",
        default=None,
    )
    timeout_message: str | None = public_field(
        description="Message used in the TimeoutError raised on exhaustion.",
        default=None,
    )

    def _attempt(self, attempt: int) -> AttemptOutcome:
        try:
            result = self.callback()
        except Exception as exc:
            # In polling mode an exception is treated as "not ready yet" and
            # the loop continues. The exception is surfaced only if exhaustion
            # is reached (via on_error_callback).
            message = self._format_exception_message(exc)
            return AttemptOutcome(
                success=False,
                value=None,
                error=exc,
                message=message,
                should_retry=True,
            )

        is_success_callback = self.is_success_callback
        if is_success_callback is not None:
            success = is_success_callback(result)
        else:
            success = result is not None

        if success:
            return AttemptOutcome(
                success=True, value=result, error=None, message="", should_retry=False
            )
        return AttemptOutcome(
            success=False, value=None, error=None, message="", should_retry=True
        )

    def _handle_exhaustion(
        self, last_error: Exception | None, last_message: str
    ) -> None:
        message = self.timeout_message or (
            f"Polling exhausted after {self.max_attempts} attempts."
        )
        raise TimeoutError(message)
