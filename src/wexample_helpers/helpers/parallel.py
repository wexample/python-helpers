from __future__ import annotations

from collections import deque
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

T = TypeVar("T")
R = TypeVar("R")

PARALLEL_DEFAULT_MAX_WORKERS = 32
"""Default thread pool size: matches Python's own ThreadPoolExecutor cap for
I/O-bound work. Generous enough to saturate filesystem and subprocess I/O on
typical machines, low enough to stay well below file descriptor and scheduler
limits. Callers can override with ``max_workers=N`` for memory-constrained or
interactive contexts."""


def parallel_for_each(
    items: Iterable[T],
    fn: Callable[[T], object],
    *,
    max_workers: int = PARALLEL_DEFAULT_MAX_WORKERS,
) -> None:
    """Like ``parallel_map`` but discards return values.

    Exceptions still propagate (the underlying ``executor.map`` is fully consumed
    before exit).
    """
    items_list = list(items)
    if not items_list:
        return
    if len(items_list) == 1:
        fn(items_list[0])
        return

    with ThreadPoolExecutor(max_workers=min(max_workers, len(items_list))) as executor:
        deque(executor.map(fn, items_list), maxlen=0)


def parallel_map(
    items: Iterable[T],
    fn: Callable[[T], R],
    *,
    max_workers: int = PARALLEL_DEFAULT_MAX_WORKERS,
) -> list[R]:
    """Apply ``fn`` to each item using a thread pool, preserving input order.

    Designed for I/O-bound work (filesystem, subprocess, network). For CPU-bound
    work, threading provides no gain due to the GIL — use ``ProcessPoolExecutor``.

    Empty input returns ``[]`` without starting a pool. Single-item input runs
    inline to avoid pool overhead. Exceptions from workers propagate to the caller.
    """
    items_list = list(items)
    if not items_list:
        return []
    if len(items_list) == 1:
        return [fn(items_list[0])]

    with ThreadPoolExecutor(max_workers=min(max_workers, len(items_list))) as executor:
        return list(executor.map(fn, items_list))
