from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

T = TypeVar("T")


@base_class
class RetryableCallbackManager:
    backoff_base_seconds: int = public_field(
        description="Base seconds for exponential backoff.", default=2
    )
    callback: Callable[[], T] = public_field(
        description="Callable executed with retry support."
    )
    max_attempts: int = public_field(
        description="Maximum number of attempts before failing.", default=3
    )
    on_error_callback: Callable[[Exception, str], None] | None = public_field(
        description="Callback invoked when giving up.", default=None
    )
    on_retry_callback: Callable[[int, int, int, Exception, str], None] | None = (
        public_field(description="Callback invoked before a retry sleep.", default=None)
    )
    on_success_callback: Callable[[int], None] | None = public_field(
        description="Callback invoked on success.", default=None
    )
    should_retry_callback: Callable[[Exception, str, int, int], bool] | None = (
        public_field(
            description="Predicate to decide if a retry should occur.", default=None
        )
    )

    def run(self) -> T:
        attempt = 0
        while True:
            attempt += 1
            try:
                result = self.callback()
                if self.on_success_callback:
                    self.on_success_callback(attempt)
                return result
            except Exception as exc:
                message = self._format_exception_message(exc)
                should_retry = attempt < self.max_attempts and self._should_retry(
                    exc, message, attempt, self.max_attempts
                )
                if should_retry:
                    delay_seconds = self._get_delay_seconds(attempt)
                    if self.on_retry_callback:
                        self.on_retry_callback(
                            attempt,
                            self.max_attempts,
                            delay_seconds,
                            exc,
                            message,
                        )
                    time.sleep(delay_seconds)
                    continue
                if self.on_error_callback:
                    self.on_error_callback(exc, message)
                raise

    def _format_exception_message(self, exc: Exception) -> str:
        stderr = getattr(exc, "stderr", None) or ""
        stdout = getattr(exc, "stdout", None) or ""
        combined = "\n".join([stderr.strip(), stdout.strip()]).strip()
        return combined or str(exc)

    def _get_delay_seconds(self, attempt: int) -> int:
        return self.backoff_base_seconds**attempt

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
