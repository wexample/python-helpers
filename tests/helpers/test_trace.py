from __future__ import annotations


def test_trace_get_frames_returns_list() -> None:
    from wexample_helpers.helpers.trace import trace_get_frames

    frames = trace_get_frames()
    assert isinstance(frames, list)
    assert len(frames) > 0


def test_trace_get_traceback_frames_returns_list() -> None:
    from wexample_helpers.helpers.trace import trace_get_traceback_frames

    try:
        raise ValueError("boom")
    except ValueError as exc:
        frames = trace_get_traceback_frames(exc.__traceback__)

    assert isinstance(frames, list)
    assert len(frames) > 0


def test_trace_format_returns_string() -> None:
    from wexample_helpers.helpers.trace import trace_format, trace_get_frames

    result = trace_format(trace_get_frames())
    assert isinstance(result, str)


def test_trace_inheritance_stack_prints_mro(capsys) -> None:
    from wexample_helpers.helpers.trace import trace_inheritance_stack

    class A:
        pass

    class B(A):
        pass

    trace_inheritance_stack(B())
    captured = capsys.readouterr()
    assert "Class inheritance stack" in captured.out
    assert "B" in captured.out
    assert "A" in captured.out


def test_trace_print_outputs(capsys) -> None:
    from wexample_helpers.helpers.trace import trace_print

    trace_print()
    captured = capsys.readouterr()
    assert captured.out != ""
