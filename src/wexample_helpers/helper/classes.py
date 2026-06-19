from __future__ import annotations

import inspect

from wexample_helpers.const.types import PathOrString


def classes_get_definition_path(instance: object) -> PathOrString:
    return inspect.getfile(type(instance))
