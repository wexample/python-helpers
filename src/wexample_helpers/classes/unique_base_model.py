from __future__ import annotations

from pydantic import BaseModel


class UniqueBaseModel(BaseModel):
    """
    TODO De-pydanticify everything
    """

    def __init_subclass__(cls, **kwargs) -> None:
        from wexample_helpers.errors.multiple_base_model_inheritance_error import MultipleBaseModelInheritanceError
        super().__init_subclass__(**kwargs)
        # Count the number of direct base classes that are subclasses of BaseModel.
        base_model_count = sum(
            1 for base in cls.__bases__ if issubclass(base, BaseModel)
        )
        if base_model_count > 1:

            raise MultipleBaseModelInheritanceError(cls)
