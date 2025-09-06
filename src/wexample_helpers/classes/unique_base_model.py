from __future__ import annotations

from pydantic import BaseModel


class UniqueBaseModel(BaseModel):
    """
    TODO De-pydanticify everything
    """

    def __init_subclass__(cls, **kwargs) -> None:
        pass