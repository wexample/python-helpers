from __future__ import annotations

import time
from typing import Callable, TypeVar

from wexample_helpers.decorator.base_class import base_class

T = TypeVar("T")


@base_class
class RetryableCallbackManager:
    def __init__(
        self,
        callback: Callable[[], T],
        *,
        max_attempts: int = 3,
        backoff_base_seconds: int = 2,
        should_retry_callback: Callable[[Exception, str, int, int], bool] | None = None,
        on_retry_callback: Callable[[int, int, int, Exception, str], None] | None = None,
        on_error_callback: Callable[[Exception, str], None] | None = None,
        on_success_callback: Callable[[int], None] | None = None,
    ) -> None:
        self._callback = callback
        self._max_attempts = max_attempts
        self._backoff_base_seconds = backoff_base_seconds
        self._should_retry_callback = should_retry_callback
        self._on_retry_callback = on_retry_callback
        self._on_error_callback = on_error_callback
        self._on_success_callback = on_success_callback

    def run(self) -> T:
        attempt = 0
        while True:
            attempt += 1
            try:
                result = self._callback()
                if self._on_success_callback:
                    self._on_success_callback(attempt)
                return result
            except Exception as exc:
                message = self._format_exception_message(exc)
                should_retry = attempt < self._max_attempts and self._should_retry(
                    exc, message, attempt, self._max_attempts
                )
                if should_retry:
                    delay_seconds = self._get_delay_seconds(attempt)
                    if self._on_retry_callback:
                        self._on_retry_callback(
                            attempt,
                            self._max_attempts,
                            delay_seconds,
                            exc,
                            message,
                        )
                    time.sleep(delay_seconds)
                    continue
                if self._on_error_callback:
                    self._on_error_callback(exc, message)
                raise

    def _should_retry(
        self,
        exc: Exception,
        message: str,
        attempt: int,
        max_attempts: int,
    ) -> bool:
        if self._should_retry_callback:
            return self._should_retry_callback(exc, message, attempt, max_attempts)
        return False

    def _get_delay_seconds(self, attempt: int) -> int:
        return self._backoff_base_seconds**attempt

    def _format_exception_message(self, exc: Exception) -> str:
        stderr = getattr(exc, "stderr", None) or ""
        stdout = getattr(exc, "stdout", None) or ""
        combined = "\n".join([stderr.strip(), stdout.strip()]).strip()
        return combined or str(exc)
