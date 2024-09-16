import re


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
