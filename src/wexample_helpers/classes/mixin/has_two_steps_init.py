from __future__ import annotations

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class HasTwoStepInit(BaseClass):
    # `is_setup` is publicly readable (no leading underscore), so it goes
    # through `public_field`. The wrapper itself is optional now that the
    # validator is back to permissive (see roadmap
    # `tighten-base-field-validator.md`), but kept because it's the right
    # convention for this codebase.
    is_setup: bool = public_field(
        default=False,
        description="True once `setup()` has been called. Two-step init pattern: cheap construction first, expensive wiring on demand.",
    )

    def setup(self) -> HasTwoStepInit:
        self.is_setup = True
        return self
