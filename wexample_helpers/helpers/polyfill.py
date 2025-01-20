from typing import Union, List, Type,TypeVar, Any

from pydantic import BaseModel

T = TypeVar('T', bound=type)


def polyfill_import(classes: Any, *args, **kwargs) -> None:
    """
    Fix this error, by importing classes for in a dummy method. These classes are actually not used anywhere :
    pydantic.errors.PydanticUserError: `ClassName` is not fully defined; you should define `Kernel`,
    then call `CountAdminCommand.model_rebuild()`.
    Using this method allow to add missing imports in file, event not used in page, and prevent auto formatters
    to consider import as useless.
    """
    pass


def polyfill_register_global(classes: Union[T, List[T], tuple[T, ...]]) -> None:
    """
    Registers classes in the global namespace to fix Pydantic type resolution issues.
    This is particularly useful when Pydantic needs to resolve forward references or
    when type hints reference classes that might not be in the current scope.

    Args:
        classes: A class, or list/tuple of classes to register in the global namespace

    Usage:
        polyfill_register_global(AbstractKernel)
        polyfill_register_global([AbstractKernel, Kernel])
        polyfill_register_global((AbstractKernel, Kernel))
    """
    import inspect

    # Convert single class to list
    if not isinstance(classes, (list, tuple)):
        classes = [classes]

    caller_globals = inspect.currentframe().f_back.f_globals
    for cls in classes:
        if not isinstance(cls, type):
            raise TypeError(f"Expected a class, got {type(cls)}")
        cls_name = cls.__name__
        caller_globals[cls_name] = cls


def polyfill_import_kernel_and_rebuild(
    pydantic_models: Union[Type[BaseModel], List[Type[BaseModel]]]
) -> None:
    # Fix import error.
    from src.utils.kernel import Kernel
    from wexample_app.utils.abstract_kernel import AbstractKernel

    polyfill_register_global([Kernel, AbstractKernel])

    # Handle both single model and list of models
    if isinstance(pydantic_models, list):
        for model in pydantic_models:
            model.model_rebuild()
    else:
        pydantic_models.model_rebuild()


def polyfill_not_implemented_error() -> None:
    import inspect

    function_name = inspect.currentframe().f_back.f_code.co_name
    raise NotImplementedError(f"{function_name} must be implemented by subclass")
