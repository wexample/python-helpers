from __future__ import annotations

import asyncio
import sys

import pytest


def test_shell_apply_sudo_elevate_in_shell_mode() -> None:
    from wexample_helpers.helper.shell import _shell_apply_sudo

    result = _shell_apply_sudo("echo x", sudo_user=None, elevate=True, shell=True)
    assert result == "sudo -- echo x"


def test_shell_apply_sudo_passthrough_without_request() -> None:
    from wexample_helpers.helper.shell import _shell_apply_sudo

    result = _shell_apply_sudo(
        ["echo", "x"], sudo_user=None, elevate=False, shell=False
    )
    assert result == ["echo", "x"]


def test_shell_apply_sudo_prefixes_user_in_list_mode() -> None:
    from wexample_helpers.helper.shell import _shell_apply_sudo

    result = _shell_apply_sudo(
        ["echo", "x"], sudo_user="bob", elevate=False, shell=False
    )
    assert result == ["sudo", "-u", "bob", "--", "echo", "x"]


def test_shell_run_async_captures_stdout() -> None:
    from wexample_helpers.helper.shell import shell_run_async

    result = asyncio.run(shell_run_async([sys.executable, "-c", "print('async-hi')"]))
    assert result.returncode == 0
    assert result.stdout.strip() == "async-hi"


def test_shell_run_captures_stdout() -> None:
    from wexample_helpers.helper.shell import shell_run

    result = shell_run([sys.executable, "-c", "print('hello')"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello"


def test_shell_run_check_false_returns_returncode() -> None:
    from wexample_helpers.helper.shell import shell_run

    result = shell_run([sys.executable, "-c", "import sys; sys.exit(3)"], check=False)
    assert result.returncode == 3


def test_shell_run_raises_on_failure() -> None:
    from wexample_helpers.exception.shell_command_failed_exception import (
        ShellCommandFailedException,
    )
    from wexample_helpers.helper.shell import shell_run

    with pytest.raises(ShellCommandFailedException, match=r"exited with code 3"):
        shell_run([sys.executable, "-c", "import sys; sys.exit(3)"])


def test_shell_split_cmd_passes_list_through() -> None:
    from wexample_helpers.helper.shell import shell_split_cmd

    assert shell_split_cmd(["echo", "hi"]) == ["echo", "hi"]


def test_shell_split_cmd_splits_string() -> None:
    from wexample_helpers.helper.shell import shell_split_cmd

    assert shell_split_cmd("echo hello world") == ["echo", "hello", "world"]


def test_shell_stream_async_invokes_stdout_callback() -> None:
    from wexample_helpers.helper.shell import shell_stream_async

    lines: list[str] = []
    rc = asyncio.run(
        shell_stream_async(
            [sys.executable, "-c", "print('streamed')"],
            on_stdout=lines.append,
        )
    )
    assert rc == 0
    assert "streamed" in "".join(lines)


def test_shell_which_finds_python() -> None:
    from wexample_helpers.helper.shell import shell_which

    assert shell_which(sys.executable) is not None or shell_which("python") is not None


def test_shell_which_returns_none_for_missing() -> None:
    from wexample_helpers.helper.shell import shell_which

    assert shell_which("definitely-not-a-real-binary-xyz") is None
