from datetime import datetime
from wexample_helpers.test.classes.pydantic_inheritance_main import PydanticInheritanceMain
from wexample_helpers.debug.debug_dump import DebugDump

def test_pydantic_inheritance():
    # Create instance with various properties
    instance = PydanticInheritanceMain(
        environment="production",
        name="test_instance",
        tags=["test", "debug"],
        description="A test instance",
        enabled=True,
        priority=50
    )
    
    # Add some metadata
    instance._metadata["custom_key"] = "custom_value"
    
    # Debug dump the instance to see how our debug handles the complex inheritance
    print("\nInstance Debug:")
    dump = DebugDump(instance)
    dump.execute()
