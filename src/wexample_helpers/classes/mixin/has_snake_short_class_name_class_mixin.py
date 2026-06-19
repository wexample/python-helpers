from __future__ import annotations

from wexample_helpers.classes.mixin.has_short_class_name_class_mixin import (
    HasShortClassNameClassMixin,
)


class HasSnakeShortClassNameClassMixin(HasShortClassNameClassMixin):
    @classmethod
    def get_name(cls) -> str:
        return cls.get_snake_short_class_name()

    @classmethod
    def get_snake_class_name_suffix(cls) -> str | None:
        suffix = cls.get_class_name_suffix()
        if suffix is None:
            return None
        from wexample_helpers.helper.string import string_to_snake_case

        return string_to_snake_case(suffix)

    @classmethod
    def get_snake_short_class_name(cls) -> str:
        from wexample_helpers.helper.string import string_to_snake_case

        return string_to_snake_case(cls.get_short_class_name())
