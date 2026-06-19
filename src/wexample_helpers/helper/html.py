from __future__ import annotations

import re

_RE_REMOVE_TAGS = re.compile(r"<[^>]*>")
_RE_SPLIT_PROMPT = re.compile(r"(<[^>]*>[^<]*<\/[^>]*>)")


def html_remove_tags(text):
    # Use a regular expression to find and remove tags
    # This regex matches anything that looks like HTML/XML tag and replaces it with an empty string
    return _RE_REMOVE_TAGS.sub("", text)


def html_split_prompt_parts(prompt_body: str) -> list[str]:
    parts = _RE_SPLIT_PROMPT.split(prompt_body)
    parts = [part for part in parts if part.strip()]
    result = []

    if not parts:
        return []

    temp_parts = [parts[0]]
    for part in parts[1:]:
        if "<" in part and ">" in part:
            temp_parts.append(part)
        else:
            result.append("".join(temp_parts))
            temp_parts = [part]
    result.append("".join(temp_parts))
    return result
