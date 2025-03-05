from pydantic import BaseModel, Field
from ..mixins.pydantic_fields_mixin import PydanticFieldsMixin
from ..mixins.pydantic_private_mixin import PydanticPrivateMixin

class PydanticInheritanceModel(PydanticFieldsMixin, PydanticPrivateMixin, BaseModel):
    """Pydantic model combining both mixins with additional functionality."""
    
    enabled: bool = Field(default=True, description="Whether the instance is enabled")
    priority: int = Field(default=0, ge=0, le=100, description="Priority level (0-100)")
    
    def __init__(self, **data):
        super().__init__(**data)
        # Initialize any mixin-specific stuff if needed
        self._metadata["initialized_at"] = self._created_at
