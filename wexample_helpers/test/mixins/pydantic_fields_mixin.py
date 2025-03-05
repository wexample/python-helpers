from typing import Optional, List
from pydantic import Field

class PydanticFieldsMixin:
    """Mixin providing public Pydantic fields without inheriting from BaseModel."""
    
    name: str = Field(description="Name of the instance")
    tags: List[str] = Field(default_factory=list, description="List of tags")
    description: Optional[str] = Field(default=None, description="Optional description")
    version: str = Field(default="1.0.0", pattern=r"^\d+\.\d+\.\d+$")
