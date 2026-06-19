from __future__ import annotations

import json
from typing import Any

from wexample_helpers.const.types import PathOrString


def json_load(path: PathOrString) -> list[Any] | dict[Any, Any]:
    with open(path) as f:
        return json.load(f)


def json_load_if_valid(path: PathOrString) -> Any | bool:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        return False


def json_parse_if_valid(json_data: PathOrString, default: Any = False) -> Any:
    try:
        return json.loads(json_data)
    except (ValueError, json.JSONDecodeError):
        return default
