from __future__ import annotations

import threading
import time

import pytest


def test_parallel_map_preserves_order() -> None:
    from wexample_helpers.helpers.parallel import parallel_map

    result = parallel_map([5, 1, 3, 2, 4], lambda x: x * 10)
    assert result == [50, 10, 30, 20, 40]


def test_parallel_map_empty() -> None:
    from wexample_helpers.helpers.parallel import parallel_map

    assert parallel_map([], lambda x: x) == []


def test_parallel_map_single_item_no_pool() -> None:
    from wexample_helpers.helpers.parallel import parallel_map

    main_thread = threading.get_ident()
    seen: list[int] = []

    def fn(x: int) -> int:
        seen.append(threading.get_ident())
        return x

    parallel_map([42], fn)
    assert seen == [main_thread]


def test_parallel_map_actually_parallel() -> None:
    from wexample_helpers.helpers.parallel import parallel_map

    items = [0.1] * 5

    def sleep_then_return(d: float) -> float:
        time.sleep(d)
        return d

    start = time.monotonic()
    parallel_map(items, sleep_then_return, max_workers=5)
    elapsed = time.monotonic() - start

    # Sequential would be ≥ 0.5s; parallel should be well under 0.3s.
    assert elapsed < 0.3, f"expected parallel execution, took {elapsed:.3f}s"


def test_parallel_map_propagates_exception() -> None:
    from wexample_helpers.helpers.parallel import parallel_map

    def boom(x: int) -> int:
        if x == 3:
            raise ValueError("boom")
        return x

    with pytest.raises(ValueError, match="boom"):
        parallel_map([1, 2, 3, 4], boom)


def test_parallel_for_each_runs_all() -> None:
    from wexample_helpers.helpers.parallel import parallel_for_each

    seen: list[int] = []
    lock = threading.Lock()

    def collect(x: int) -> None:
        with lock:
            seen.append(x)

    parallel_for_each([1, 2, 3, 4, 5], collect)
    assert sorted(seen) == [1, 2, 3, 4, 5]


def test_parallel_for_each_empty() -> None:
    from wexample_helpers.helpers.parallel import parallel_for_each

    parallel_for_each([], lambda _: None)
