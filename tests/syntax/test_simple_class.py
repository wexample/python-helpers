import unittest
from wexample_helpers.test.classes.simple_class import SimpleObject
from wexample_helpers.helpers.debug import debug_dump

class TestSimpleObject(unittest.TestCase):
    def test_instance_creation(self):
        obj1 = SimpleObject()
        self.assertIsInstance(obj1, SimpleObject)
        self.assertEqual(obj1.name, "default")
        
        obj2 = SimpleObject(name="test")
        self.assertIsInstance(obj2, SimpleObject)
        self.assertEqual(obj2.name, "test")
        
        # Test debug_dump
        debug_dump(obj1)
        debug_dump(obj2)
        debug_dump(SimpleObject)
