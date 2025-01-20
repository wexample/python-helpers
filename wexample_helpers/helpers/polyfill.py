from typing import Any


def polyfill_import(classes: Any) -> None:
    """
    Fix this error, by importing classes for in a dummy method. These classes are actually not used anywhere :
    pydantic.errors.PydanticUserError: `ClassName` is not fully defined; you should define `Kernel`,
    then call `CountAdminCommand.model_rebuild()`.
    Using this method allow to add missing imports in file, event not used in page, and prevent auto formatters
    to consider import as useless.
    """
    pass

def polyfill_not_implemented_error() -> None:
    import inspect

    function_name = inspect.currentframe().f_back.f_code.co_name
    raise NotImplementedError(f"{function_name} must be implemented by subclass")
