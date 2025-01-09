import re
from typing import List


def string_to_kebab_case(text: str) -> str:
    """
    Convert text to kebab case, converting spaces and underscores to dashes.
    """
    return re.sub(r"[_\s]+", "-", re.sub(r"([a-z])([A-Z])", r"\1-\2", text)).lower()


def string_to_snake_case(text: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    s2 = re.sub("([a-z])([A-Z])", r"\1_\2", s1).lower()
    s3 = re.sub("([0-9])([A-Z])", r"\1\2", s2)
    return str(re.sub(r"\W+", "_", s3))


def string_append_missing_lines(lines: List[str], content: str) -> str:
    # Split the current content into lines
    current_lines = content.splitlines()

    # Determine the lines that need to be added
    lines_to_add = [line for line in lines if line not in current_lines]

    if lines_to_add:
        # Ensure the content ends with a newline before appending new lines
        if content and not content.endswith('\n'):
            content += '\n'
        # Add the missing lines
        content += '\n'.join(lines_to_add) + '\n'

    return content
