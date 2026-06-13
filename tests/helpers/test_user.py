from __future__ import annotations

import os


def test_user_get_real_uid_uses_sudo_uid(monkeypatch) -> None:
    from wexample_helpers.helpers.user import user_get_real_uid

    monkeypatch.setenv("SUDO_UID", "4242")
    assert user_get_real_uid() == 4242


def test_user_get_real_uid_falls_back_to_os(monkeypatch) -> None:
    from wexample_helpers.helpers.user import user_get_real_uid

    monkeypatch.delenv("SUDO_UID", raising=False)
    assert user_get_real_uid() == os.getuid()


def test_user_get_real_gid_uses_sudo_gid(monkeypatch) -> None:
    from wexample_helpers.helpers.user import user_get_real_gid

    monkeypatch.setenv("SUDO_GID", "4343")
    assert user_get_real_gid() == 4343


def test_user_get_real_gid_falls_back_to_os(monkeypatch) -> None:
    from wexample_helpers.helpers.user import user_get_real_gid

    monkeypatch.delenv("SUDO_GID", raising=False)
    assert user_get_real_gid() == os.getgid()


def test_user_get_real_username_prefers_sudo_user(monkeypatch) -> None:
    from wexample_helpers.helpers.user import user_get_real_username

    monkeypatch.setenv("SUDO_USER", "alice")
    assert user_get_real_username() == "alice"


def test_user_get_real_username_falls_back_to_user(monkeypatch) -> None:
    from wexample_helpers.helpers.user import user_get_real_username

    monkeypatch.delenv("SUDO_USER", raising=False)
    monkeypatch.setenv("USER", "bob")
    assert user_get_real_username() == "bob"
