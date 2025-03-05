import unittest
from wexample_helpers.test.classes.simple_class import SimpleObject

class TestSimpleObject(unittest.TestCase):
    def test_instance_creation(self):
        obj1 = SimpleObject()
        self.assertIsInstance(obj1, SimpleObject)
        self.assertEqual(obj1.name, "default")
        
        obj2 = SimpleObject(name="test")
        self.assertIsInstance(obj2, SimpleObject)
        self.assertEqual(obj2.name, "test")
