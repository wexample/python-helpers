from __future__ import annotations

import re
import secrets
import string as _string
from collections.abc import Callable
from functools import cache, lru_cache

# Pre-compiled regex patterns for string_detect_case
_RE_DETECT_CONSTANT = re.compile(r"^[A-Z][A-Z0-9_]*$")
_RE_DETECT_SNAKE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")
_RE_DETECT_KEBAB = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
_RE_DETECT_DOT = re.compile(r"^[a-z][a-z0-9]*(\.[a-z0-9]+)*$")
_RE_DETECT_PATH = re.compile(r"^[a-z][a-z0-9]*(/[a-z0-9]+)*$")
_RE_DETECT_CAMEL_FULL = re.compile(r"^[a-z][a-zA-Z0-9]*$")
_RE_DETECT_CAMEL_UPPER = re.compile(r"[A-Z]")
_RE_DETECT_PASCAL = re.compile(r"^[A-Z][a-zA-Z0-9]*$")
_RE_DETECT_TITLE = re.compile(r"^[A-Z][a-z]+(\s[A-Z][a-z]+)*$")
_RE_DETECT_MIXED = re.compile(r"[a-z][A-Z]")

# Pre-compiled regex patterns for _normalize
_RE_NORM_SEP = re.compile(r"[^A-Za-z0-9]+")
_RE_NORM_CAMEL = re.compile(r"([a-z0-9])([A-Z])")
_RE_NORM_UPPER = re.compile(r"([A-Z]+)([A-Z][a-z])")

# CSI sequences (colors, styles) and OSC 8 hyperlinks, for string_strip_ansi
_RE_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]|\x1b\]8;;[^\x1b]*\x1b\\")

# Alphabet constant for string_random_token
_RANDOM_TOKEN_ALPHABET = _string.ascii_letters + _string.digits

# Lorem ipsum base text and its length for string_generate_lorem_ipsum
_LOREM_BASE = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
    "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
)
_LOREM_BASE_LEN = len(_LOREM_BASE)


def string_append_missing_lines(lines: list[str], content: str) -> str:
    # Normalize content by removing trailing empty lines for consistent comparison
    content = string_remove_trailing_empty_lines(content)

    # Split the current content into lines
    current_lines = content.splitlines()

    # Determine the lines that need to be added (deduplicate to avoid adding same line multiple times)
    lines_to_add = []
    seen = set(current_lines)
    for line in lines:
        if line not in seen:
            lines_to_add.append(line)
            seen.add(line)

    if lines_to_add:
        # Ensure the content ends with a newline before appending new lines
        content = string_ensure_end_with_new_line(content)
        # Add the missing lines
        content += "\n".join(lines_to_add) + "\n"

    return content


def string_capitalize_first(text: str) -> str:
    """
    Capitalize only the first letter of the string (safe version).
    """
    return text[:1].upper() + text[1:] if text else text


def string_convert_case(text: str, to_format: str) -> str:
    """
    Convert text to any case format.

    :param text: The string to convert
    :param to_format: Target format - one of: 'snake', 'kebab', 'camel', 'pascal', 'constant', 'title', 'dot', 'path'
    :return: Converted string
    :raises ValueError: If to_format is not recognized
    """
    converters = string_convert_case_map()

    if to_format not in converters:
        valid_formats = ", ".join(converters.keys())
        raise ValueError(
            f"Invalid format '{to_format}'. Must be one of: {valid_formats}"
        )

    return converters[to_format](text)


@cache
def string_convert_case_map() -> dict[str, Callable[[str], str]]:
    return {
        "snake": string_to_snake_case,
        "kebab": string_to_kebab_case,
        "camel": string_to_camel_case,
        "pascal": string_to_pascal_case,
        "constant": string_to_constant_case,
        "title": string_to_title_case,
        "dot": string_to_dot_case,
        "path": string_to_path_case,
    }


@lru_cache(maxsize=512)
def string_detect_case(text: str) -> str:
    """
    Detect the case format of a string.

    :param text: The string to analyze
    :return: One of: 'snake', 'kebab', 'camel', 'pascal', 'constant', 'title', 'dot', 'path', 'mixed', 'unknown'
    """
    text = text.strip()
    if not text:
        return "unknown"

    # Check for specific patterns
    if _RE_DETECT_CONSTANT.match(text):
        return "constant"
    if _RE_DETECT_SNAKE.match(text):
        return "snake"
    if _RE_DETECT_KEBAB.match(text):
        return "kebab"
    if _RE_DETECT_DOT.match(text):
        return "dot"
    if _RE_DETECT_PATH.match(text):
        return "path"
    if _RE_DETECT_CAMEL_FULL.match(text) and _RE_DETECT_CAMEL_UPPER.search(text):
        return "camel"
    if _RE_DETECT_PASCAL.match(text):
        return "pascal"
    if _RE_DETECT_TITLE.match(text):
        return "title"

    # Check for mixed separators
    separators = sum(
        (
            "_" in text,
            "-" in text,
            "." in text,
            "/" in text,
            bool(_RE_DETECT_MIXED.search(text)),
        )
    )

    if separators > 1:
        return "mixed"

    return "unknown"


def string_ensure_end_with_new_line(text: str) -> str:
    return text if text.endswith("\n") else text + "\n"


def string_generate_lorem_ipsum(length: int = 100) -> str:
    if length <= 0:
        return ""

    text = (_LOREM_BASE + " ") * ((length // (_LOREM_BASE_LEN + 1)) + 1)

    cut = text[:length].rstrip()

    if (
        len(cut) == length
        and length < len(text)
        and not cut.endswith((" ", ".", ",", "!", "?", ";", ":"))
    ):
        last_space = cut.rfind(" ")
        if last_space > 0:
            cut = cut[:last_space]

    return cut.strip()


def string_is_camel_case(text: str) -> bool:
    """Check if text is in camelCase format."""
    return string_detect_case(text) == "camel"


def string_is_constant_case(text: str) -> bool:
    """Check if text is in CONSTANT_CASE format."""
    return string_detect_case(text) == "constant"


def string_is_dot_case(text: str) -> bool:
    """Check if text is in dot.case format."""
    return string_detect_case(text) == "dot"


def string_is_kebab_case(text: str) -> bool:
    """Check if text is in kebab-case format."""
    return string_detect_case(text) == "kebab"


def string_is_pascal_case(text: str) -> bool:
    """Check if text is in PascalCase format."""
    return string_detect_case(text) == "pascal"


def string_is_path_case(text: str) -> bool:
    """Check if text is in path/case format."""
    return string_detect_case(text) == "path"


def string_is_snake_case(text: str) -> bool:
    """Check if text is in snake_case format."""
    return string_detect_case(text) == "snake"


def string_is_title_case(text: str) -> bool:
    """Check if text is in Title Case format."""
    return string_detect_case(text) == "title"


def string_random_token(length: int = 24) -> str:
    return "".join(secrets.choice(_RANDOM_TOKEN_ALPHABET) for _ in range(length))


def string_remove_prefix(string: str, prefix: str) -> str:
    """
    Remove a prefix from a string if it exists at the beginning.

    :param string: The string to process
    :param prefix: The prefix to remove
    :return: String with prefix removed if found at start
    """
    return string.removeprefix(prefix)


def string_remove_trailing_empty_lines(content: str) -> str:
    """
    Remove trailing empty lines from content while preserving the final newline if present.

    :param content: The string content to normalize
    :return: Content with trailing empty lines removed
    """
    if not content:
        return content

    lines = content.splitlines()
    # Remove trailing empty lines
    while lines and not lines[-1].strip():
        lines.pop()

    # Rejoin and preserve final newline if original had one
    result = "\n".join(lines)
    if result and content.endswith("\n"):
        result += "\n"

    return result


def string_render_boolean(boolean: bool) -> str:
    return "True" if boolean else "False"


def string_replace_params(text: str, params: dict) -> str:
    """
    Replace parameters in a text string with values from a dictionary.
    Each parameter in the text should be in the format %param_name%.
    Example:
        text = "Hello %name%, you are %age% years old"
        params = {"name": "John", "age": "30"}
        result = "Hello John, you are 30 years old"
    """
    result = text
    for key, value in params.items():
        result = result.replace(f"%{key}%", str(value))
    return result


def string_strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences (colors, styles, hyperlinks) from a string.

    For text that was rendered for a terminal but is about to be compared,
    parsed or stored, where the escape bytes are invisible noise that silently
    breaks equality."""
    return _RE_ANSI_ESCAPE.sub("", text)


@lru_cache(maxsize=512)
def string_to_camel_case(text: str) -> str:
    """
    Convert text to camelCase (e.g. 'my_example_string' -> 'myExampleString').
    """
    words = _normalize(text)
    if not words:
        return ""
    return words[0] + "".join(w.capitalize() for w in words[1:])


@lru_cache(maxsize=512)
def string_to_constant_case(text: str) -> str:
    """
    Convert text to CONSTANT_CASE (e.g. "MyClassName" -> "MY_CLASS_NAME").
    """
    return "_".join(_normalize(text)).upper()


@lru_cache(maxsize=512)
def string_to_dot_case(text: str) -> str:
    """
    Convert text to dot.case (e.g. "MyClassName" -> "my.class.name").
    Useful for configuration keys and namespaces.
    """
    return ".".join(_normalize(text))


@lru_cache(maxsize=512)
def string_to_kebab_case(text: str) -> str:
    """
    Convert text to kebab-case (e.g. "MyClassName" -> "my-class-name").
    """
    return "-".join(_normalize(text))


@lru_cache(maxsize=512)
def string_to_pascal_case(text: str) -> str:
    """
    Convert text to PascalCase (ClassCase), e.g. 'my_example_string' -> 'MyExampleString'.
    """
    return "".join(w.capitalize() for w in _normalize(text))


@lru_cache(maxsize=512)
def string_to_path_case(text: str) -> str:
    """
    Convert text to path/case (e.g. "MyClassName" -> "my/class/name").
    Useful for file paths and URL segments.
    """
    return "/".join(_normalize(text))


@lru_cache(maxsize=512)
def string_to_snake_case(text: str) -> str:
    """
    Convert text to snake_case (e.g. "MyClassName" -> "my_class_name").
    """
    return "_".join(_normalize(text))


@lru_cache(maxsize=512)
def string_to_title_case(text: str) -> str:
    """
    Convert text to Title Case (capitalize first letter of each word).
    """
    return " ".join(w.capitalize() for w in _normalize(text))


def string_truncate(text: str, limit: int) -> str:
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text


@lru_cache(maxsize=512)
def _normalize(value: str) -> tuple[str, ...]:
    """
    Convert any string into a normalized tuple of lowercase words.
    Handles:
    - camelCase / PascalCase
    - snake_case
    - kebab-case
    - dotted.case
    - path/case
    - mixed separators
    """

    if not value:
        return ()

    # Trim whitespace
    value = value.strip()

    # Replace all non-alphanumeric separators with space
    value = _RE_NORM_SEP.sub(" ", value)

    # Split camelCase / PascalCase
    value = _RE_NORM_CAMEL.sub(r"\1 \2", value)

    # Split multiple caps like "JSONParser" → "JSON Parser"
    value = _RE_NORM_UPPER.sub(r"\1 \2", value)

    # Normalize spaces and remove empty segments
    return tuple(value.lower().split())
