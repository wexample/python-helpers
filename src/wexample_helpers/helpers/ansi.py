from __future__ import annotations


def ansi_center(text: str, width: int, fillchar: str = " ") -> str:
    """Center text by visible width.

    Padding is added outside of any ANSI/OSC sequences in `text` by
    pre/append fill characters, so links (OSC 8) and colors remain intact
    and margins aren't part of hyperlinks.
    """
    w = ansi_display_width(text)
    if w >= width:
        return text

    left = (width - w) // 2
    right = width - w - left
    return (fillchar * left) + text + (fillchar * right)


def ansi_display_width(text: str) -> int:
    """Compute the visible display width of text.

    Strips ANSI CSI and OSC 8 sequences, then measures width with wcwidth
    to handle emojis, combining marks, and double-width (CJK) characters.
    """
    from wcwidth import wcwidth

    visible = ansi_strip_invisible(text)
    return sum(max(wcwidth(ch), 0) for ch in visible)


def ansi_strip(text: str) -> str:
    """Remove ANSI escape sequences (CSI) from the text using shared constants."""
    from wexample_helpers.const.ansi import CSI_RE

    return CSI_RE.sub("", text)


def ansi_strip_invisible(text: str) -> str:
    return ansi_strip(ansi_strip_osc(text))


def ansi_strip_osc(text: str) -> str:
    from wexample_helpers.const.ansi import OSC8_RE

    return OSC8_RE.sub("", text)


def ansi_truncate_visible(text: str, max_width: int) -> str:
    from wcwidth import wcwidth

    if max_width <= 0:
        return ""
    plain = ansi_strip_invisible(text)
    out_chars = []
    current = 0
    for ch in plain:
        w = max(wcwidth(ch), 0)
        if current + w > max_width:
            return "".join(out_chars)
        out_chars.append(ch)
        current += w
    return text
