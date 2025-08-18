def ansi_strip(text: str) -> str:
    """Remove ANSI escape sequences from the text."""

    import re
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)