from __future__ import annotations

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class HasTwoStepInit(BaseClass):
    # `is_setup` must go through `private_field` (not a bare `bool = False`) —
    # `BaseClass.__init_subclass__` enforces that every declared field inherits
    # from `BaseField`. The check was silently bypassed before a base_class.py
    # cleanup tightened it; this file just hadn't been updated.
    is_setup: bool = private_field(
        default=False,
        description="True once `setup()` has been called. Two-step init pattern: cheap construction first, expensive wiring on demand.",
    )

    def setup(self) -> HasTwoStepInit:
        self.is_setup = True
        return self
