import pytest
from pydantic import BaseModel

from wexample_helpers.errors.multiple_base_model_inheritance_error import MultipleBaseModelInheritanceError
from wexample_helpers.test.classes.unique_base_model_child import UniqueBaseModelChild
from wexample_helpers.debug.debug_dump import DebugDump


def test_unique_base_model():
    """Test a valid child class of UniqueBaseModel."""
    
    # Create instance
    instance = UniqueBaseModelChild(
        name="custom_name",
        value=100,
        description="Custom description"
    )

    # Test invalid inheritance
    with pytest.raises(MultipleBaseModelInheritanceError):
        # This will try to create an invalid class
        class InvalidModel(UniqueBaseModelChild, BaseModel):
            pass
    
    # Debug dump the instance
    print("\nInstance Debug:")
    dump = DebugDump(instance)
    dump.execute()
