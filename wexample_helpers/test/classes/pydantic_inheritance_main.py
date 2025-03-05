from typing import Dict, Any
from .pydantic_inheritance_config import PydanticInheritanceConfig
from .pydantic_inheritance_model import PydanticInheritanceModel

class PydanticInheritanceMain(PydanticInheritanceConfig, PydanticInheritanceModel):
    """Main class demonstrating multiple inheritance with Pydantic and mixins."""
    
    def __init__(self, **data):
        PydanticInheritanceConfig.__init__(self, environment=data.pop("environment", "development"))
        PydanticInheritanceModel.__init__(self, **data)
    
    def get_full_state(self) -> Dict[str, Any]:
        """Get the complete state combining all inherited properties."""
        return {
            "environment": self.environment,
            "name": self.name,
            "version": self.version,
            "tags": self.tags,
            "description": self.description,
            "enabled": self.enabled,
            "priority": self.priority,
            "created_at": self.created_at,
            "metadata": self.get_metadata()
        }
