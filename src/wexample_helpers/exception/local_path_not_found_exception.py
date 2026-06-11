from __future__ import annotations

from typing import ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.exception.undefined_exception import UndefinedException


@base_class
class LocalPathNotFoundException(UndefinedException):
    error_code: ClassVar[str] = "LOCAL_PATH_NOT_FOUND"

    path: object = public_field(default=None, description="Offending file system path")

    def _build_message(self) -> str:
        return f"Path does not exist: {self.path}"
