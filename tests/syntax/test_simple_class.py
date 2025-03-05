import unittest
from wexample_helpers.test.classes.simple_class import SimpleObject
from wexample_helpers.debug.debug_dump import DebugDump
from wexample_helpers.debug.debug_dump_class import DebugDumpClass

class TestSimpleObject(unittest.TestCase):
    def test_simple_object(self):
        # Test instance creation with default values
        obj1 = SimpleObject()
        self.assertIsInstance(obj1, SimpleObject)
        self.assertEqual(obj1.name, "default")
        
        # Test instance creation with custom values
        obj2 = SimpleObject(name="test")
        self.assertIsInstance(obj2, SimpleObject)
        self.assertEqual(obj2.name, "test")
        
        # Test debug dump of class structure
        class_dumper = DebugDumpClass(SimpleObject)
        class_dumper.collect_data()
        class_data = class_dumper.data
        
        # Verify class structure
        self.assertEqual(class_data["type"], "class")
        self.assertEqual(class_data["name"], "SimpleObject")
        
        # Test debug dump of instance
        instance_dumper = DebugDump(obj2)
        instance_dumper.collect_data()
        instance_data = instance_dumper.data
        
        # Verify instance data
        self.assertTrue("instance_of" in instance_data)
        self.assertEqual(instance_data["instance_of"], "SimpleObject")
        self.assertTrue("attributes" in instance_data)
        attrs = instance_data["attributes"]
        self.assertTrue("name" in attrs)
        self.assertEqual(attrs["name"]["value"], "'test'")
        
        # Print debug outputs for visual verification
        class_dumper.print()
        instance_dumper.print()
