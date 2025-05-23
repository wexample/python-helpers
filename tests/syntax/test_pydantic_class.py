from datetime import datetime
from wexample_helpers.test.classes.pydantic_class import PydanticClass
from wexample_helpers.debug.debug_dump import DebugDump

def test_pydantic_class():
    # Create instance with some data
    instance = PydanticClass(
        name="test_item",
        count=42,
        description="A test item",
        tags=["test", "debug"],
        created_at=datetime(2025, 3, 5, 15, 46)
    )
    
    # Dump the instance
    dump = DebugDump(instance)
    dump.execute()
