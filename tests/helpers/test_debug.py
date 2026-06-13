from __future__ import annotations

import pytest


def test_dd_exits() -> None:
    from wexample_helpers.helpers.debug import dd

    with pytest.raises(SystemExit):
        dd("x")


def test_debug_dump_and_die_exits() -> None:
    from wexample_helpers.helpers.debug import debug_dump_and_die

    with pytest.raises(SystemExit):
        debug_dump_and_die({"a": 1})


def test_debug_dump_runs(capsys) -> None:
    from wexample_helpers.helpers.debug import debug_dump

    debug_dump({"a": 1})
    captured = capsys.readouterr()
    assert captured.out != ""


def test_debug_timer_end_pops_timer() -> None:
    from wexample_helpers.helpers.debug import debug_timer_end, debug_timer_start

    debug_timer_start("once")
    debug_timer_end("once")
    assert debug_timer_end("once") is None


def test_debug_timer_end_returns_none_for_unknown() -> None:
    from wexample_helpers.helpers.debug import debug_timer_end

    assert debug_timer_end("never-started") is None


def test_debug_timer_measures_elapsed() -> None:
    from wexample_helpers.helpers.debug import debug_timer_end, debug_timer_start

    debug_timer_start("sample")
    elapsed = debug_timer_end("sample")
    assert elapsed is not None
    assert elapsed >= 0
