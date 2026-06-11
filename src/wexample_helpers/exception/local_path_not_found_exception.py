from __future__ import annotations

from typing import ClassVar

from attrs import Factory

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.exception.undefined_exception import UndefinedException


@base_class
class LocalPathNotFoundException(UndefinedException):
    error_code: ClassVar[str] = "LOCAL_PATH_NOT_FOUND"

    path: object = public_field(default=None, description="Offending file system path")
    message: str = public_field(
        default=Factory(
            lambda self: f"Path does not exist: {self.path}", takes_self=True
        ),
        description="Human-readable error message",
    )
