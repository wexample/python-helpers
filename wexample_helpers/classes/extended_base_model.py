from wexample_helpers.classes.mixin.printable_mixin import PrintableMixin
from wexample_helpers.classes.unique_base_model import UniqueBaseModel
from typing import NoReturn, Optional
import inspect


class ExtendedBaseModel(PrintableMixin, UniqueBaseModel):
    @classmethod
    def __raise_not_implemented_error(
        cls,
        method: Optional[str] = None,
        message: Optional[str] = None,
    ) -> NoReturn:
        """Convenience to raise a standardized NotImplementedError.

        Usage in would-be abstract methods:

            def do_work(self):
                self.__class__.__raise_not_implemented_error()

        or, from instance methods:

            def do_work(self):
                type(self).__raise_not_implemented_error()

        The method name is inferred from the caller if not provided.
        """
        if method is None:
            try:
                method = inspect.stack()[1].function
            except Exception:
                method = "<unknown>"
        raise NotImplementedError(message or f"{cls.__name__}.{method} must be implemented by subclass")

    def __getattr__(self, item):
        try:
            return super().__getattr__(item)
        except AttributeError:
            # Special diagnostic for pydantic initialization issues
            if item == "__pydantic_private__":
                cls_name = type(self).__name__
                msg = (
                    f"{cls_name} is not fully initialized by Pydantic: missing '__pydantic_private__'.\n"
                    "This typically happens when a mixin defines __init__ and is initialized before BaseModel.\n"
                    "Fix: in your class __init__, call BaseModel.__init__(self, **kwargs) first, then your mixins;\n"
                    "or move mixin initialization logic to a post-init hook."
                )
                raise AttributeError(msg) from None

            cls_name = type(self).__name__
            raise AttributeError(f"{cls_name} has no attribute '{item}'") from None

    @classmethod
    def _raise_not_implemented_error(
        cls,
        method: Optional[str] = None,
        message: Optional[str] = None,
    ) -> NoReturn:
        """Public-friendly alias without name mangling.

        Prefer this helper when calling from subclasses to avoid double-underscore
        name-mangling issues.
        """
        cls.__raise_not_implemented_error(method=method, message=message)
