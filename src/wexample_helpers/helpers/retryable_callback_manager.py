from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.helpers.abstract_attempt_manager import (
    AbstractAttemptManager,
    AttemptOutcome,
)

T = TypeVar("T")


@base_class
class RetryableCallbackManager(AbstractAttemptManager[T]):
    """Run a callback with retry-on-exception semantics.

    The callback is retried when it raises and `should_retry_callback` returns
    True. On exhaustion (or when retry is declined), the original exception is
    re-raised.
    """

    callback: Callable[[], T] = public_field(
        description="Callable executed with retry support."
    )
    should_retry_callback: Callable[[Exception, str, int, int], bool] | None = (
        public_field(
            description="Predicate to decide if a retry should occur on exception.",
            default=None,
        )
    )

    def _attempt(self, attempt: int) -> AttemptOutcome:
        try:
            result = self.callback()
        except Exception as exc:
            message = self._format_exception_message(exc)
            cb = self.should_retry_callback
            should_retry = (
                cb(exc, message, attempt, self.max_attempts) if cb is not None else False
            )
            return AttemptOutcome(
                success=False,
                value=None,
                error=exc,
                message=message,
                should_retry=should_retry,
            )
        return AttemptOutcome(
            success=True, value=result, error=None, message="", should_retry=False
        )

    def _handle_exhaustion(
        self, last_error: Exception | None, last_message: str
    ) -> None:
        if last_error is None:
            raise RuntimeError("RetryableCallbackManager exhausted without an error.")
        raise last_error
