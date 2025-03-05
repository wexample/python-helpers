from typing import Optional, List


class PydanticFieldsMixin:
    """Mixin providing public Pydantic fields without inheriting from BaseModel."""

    name: str
    tags: List[str]
    description: Optional[str]
    version: str = "1.0.0"
