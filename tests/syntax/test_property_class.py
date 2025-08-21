from wexample_helpers.test.classes.property_class import PropertyClass
from wexample_helpers.common.debug.debug_dump import DebugDump


def test_property_class():
    # Create instance
    instance = PropertyClass()

    # Set value through property
    instance.value = "test"

    # Dump the instance
    dump = DebugDump(instance)
    dump.execute()
