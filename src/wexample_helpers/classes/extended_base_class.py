from __future__ import annotations

import inspect
from typing import NoReturn

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.mixin.printable_mixin import PrintableMixin


class ExtendedBaseClass(PrintableMixin, BaseClass):
    def __getattr__(self, item):
        try:
            return super().__getattr__(item)
        except AttributeError:
            cls_name = type(self).__name__
            raise AttributeError(f"{cls_name} has no attribute '{item}'") from None

    @classmethod
    def _raise_not_implemented_error(
        cls,
        method: str | None = None,
        message: str | None = None,
    ) -> NoReturn:
        """Convenience to raise a standardized NotImplementedError.

        Usage in would-be abstract/class methods:

            @classmethod
            def get_example_class(cls):
                cls._raise_not_implemented_error()

        or, from instance methods:

            def do_work(self):
                type(self)._raise_not_implemented_error()

        The method name is inferred from the caller if not provided.
        """
        if method is None:
            try:
                method = inspect.stack()[1].function
            except Exception:
                method = "<unknown>"
        raise NotImplementedError(
            message or f"{cls.__name__}.{method} must be implemented by subclass"
        )
