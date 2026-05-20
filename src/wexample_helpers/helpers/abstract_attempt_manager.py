from __future__ import annotations

import time
from collections.abc import Callable
from typing import Generic, NamedTuple, TypeVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

T = TypeVar("T")


class AttemptOutcome(NamedTuple):
    """Result of a single attempt within an AbstractAttemptManager loop."""

    error: Exception | None
    message: str
    should_retry: bool
    success: bool
    value: object | None


@base_class
class AbstractAttemptManager(Generic[T]):
    """Shared loop for attempt-based managers (retry-on-exception, poll-until-success, ...).

    Subclasses implement two hooks:
      - `_attempt(attempt)` runs one tentative and returns an AttemptOutcome.
      - `_handle_exhaustion(last_error, last_message)` raises when all attempts
        are exhausted (must raise; the manager never returns from there).
    """

    backoff_base_seconds: int = public_field(
        description="Base seconds for exponential backoff (delay = base ** attempt). Ignored if `delay_seconds_callback` is set.",
        default=2,
    )
    delay_seconds_callback: Callable[[int], int] | None = public_field(
        description="Optional override for delay calculation. Receives the current attempt number and returns the seconds to sleep.",
        default=None,
    )
    max_attempts: int = public_field(
        description="Maximum number of attempts before giving up.", default=3
    )
    on_error_callback: Callable[[Exception, str], None] | None = public_field(
        description="Invoked once with the last error before exhaustion handling.",
        default=None,
    )
    on_retry_callback: Callable[[int, int, int, Exception | None, str], None] | None = (
        public_field(
            description="Invoked before each retry sleep with (attempt, max_attempts, delay, error, message).",
            default=None,
        )
    )
    on_success_callback: Callable[[int], None] | None = public_field(
        description="Invoked on success with the attempt count.", default=None
    )

    def run(self) -> T:
        last_error: Exception | None = None
        last_message: str = ""

        for attempt in range(1, self.max_attempts + 1):
            outcome = self._attempt(attempt)

            if outcome.success:
                if self.on_success_callback:
                    self.on_success_callback(attempt)
                return outcome.value  # type: ignore[return-value]

            last_error, last_message = outcome.error, outcome.message

            if attempt >= self.max_attempts or not outcome.should_retry:
                break

            delay = self._get_delay_seconds(attempt)
            if self.on_retry_callback:
                self.on_retry_callback(
                    attempt,
                    self.max_attempts,
                    delay,
                    outcome.error,
                    outcome.message,
                )
            time.sleep(delay)

        if last_error is not None and self.on_error_callback:
            self.on_error_callback(last_error, last_message)

        self._handle_exhaustion(last_error, last_message)
        # Defensive: _handle_exhaustion must raise.
        raise RuntimeError("AbstractAttemptManager._handle_exhaustion must raise.")

    def _attempt(self, attempt: int) -> AttemptOutcome:
        raise NotImplementedError

    def _format_exception_message(self, exc: Exception) -> str:
        stderr = getattr(exc, "stderr", None) or ""
        stdout = getattr(exc, "stdout", None) or ""
        combined = "\n".join([stderr.strip(), stdout.strip()]).strip()
        return combined or str(exc)

    def _get_delay_seconds(self, attempt: int) -> int:
        if self.delay_seconds_callback is not None:
            return self.delay_seconds_callback(attempt)
        return self.backoff_base_seconds**attempt

    def _handle_exhaustion(
        self, last_error: Exception | None, last_message: str
    ) -> None:
        raise NotImplementedError
