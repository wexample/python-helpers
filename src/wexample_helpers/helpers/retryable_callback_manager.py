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
            should_retry = self._should_retry(exc, message, attempt, self.max_attempts)
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

    def _should_retry(
        self,
        exc: Exception,
        message: str,
        attempt: int,
        max_attempts: int,
    ) -> bool:
        if self.should_retry_callback:
            return self.should_retry_callback(exc, message, attempt, max_attempts)
        return False
