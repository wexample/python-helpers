from __future__ import annotations

CSI_RED = "\x1b[31m"
CSI_RESET = "\x1b[0m"


def test_ansi_center_pads_evenly() -> None:
    from wexample_helpers.helper.ansi import ansi_center

    assert ansi_center("ab", 6) == "  ab  "


def test_ansi_center_returns_text_when_wider_than_width() -> None:
    from wexample_helpers.helper.ansi import ansi_center

    assert ansi_center("abcdef", 3) == "abcdef"


def test_ansi_center_uses_fillchar() -> None:
    from wexample_helpers.helper.ansi import ansi_center

    assert ansi_center("ab", 6, fillchar="*") == "**ab**"


def test_ansi_display_width_counts_cjk_as_double() -> None:
    from wexample_helpers.helper.ansi import ansi_display_width

    assert ansi_display_width("中") == 2


def test_ansi_display_width_ignores_escape_sequences() -> None:
    from wexample_helpers.helper.ansi import ansi_display_width

    assert ansi_display_width(f"{CSI_RED}abc{CSI_RESET}") == 3


def test_ansi_strip_invisible_removes_both_csi_and_osc() -> None:
    from wexample_helpers.helper.ansi import ansi_strip_invisible

    text = f"{CSI_RED}{_osc8('http://x', 'link')}{CSI_RESET}"
    assert ansi_strip_invisible(text) == "link"


def test_ansi_strip_keeps_plain_text() -> None:
    from wexample_helpers.helper.ansi import ansi_strip

    assert ansi_strip("hello") == "hello"


def test_ansi_strip_osc_removes_hyperlink_wrappers() -> None:
    from wexample_helpers.helper.ansi import ansi_strip_osc

    assert ansi_strip_osc(_osc8("http://x", "link")) == "link"


def test_ansi_strip_removes_csi() -> None:
    from wexample_helpers.helper.ansi import ansi_strip

    assert ansi_strip(f"{CSI_RED}hello{CSI_RESET}") == "hello"


def test_ansi_truncate_visible_returns_empty_on_zero_width() -> None:
    from wexample_helpers.helper.ansi import ansi_truncate_visible

    assert ansi_truncate_visible("abc", 0) == ""


def test_ansi_truncate_visible_returns_text_when_short_enough() -> None:
    from wexample_helpers.helper.ansi import ansi_truncate_visible

    assert ansi_truncate_visible("abc", 10) == "abc"


def test_ansi_truncate_visible_truncates_by_width() -> None:
    from wexample_helpers.helper.ansi import ansi_truncate_visible

    assert ansi_truncate_visible("abcdef", 3) == "abc"


def _osc8(url: str, text: str) -> str:
    return f"\x1b]8;;{url}\x1b\\{text}\x1b]8;;\x1b\\"
