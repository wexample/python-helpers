import unittest
from wexample_helpers.test.classes.parent_class import ParentClass
from wexample_helpers.test.classes.child_class import ChildClass
from wexample_helpers.helpers.debug import debug_dump

class TestInheritance(unittest.TestCase):
    def test_inheritance_debug(self):
        # Create instances
        parent = ParentClass(parent_value="custom_parent")
        child = ChildClass(child_value="custom_child", parent_value="inherited_parent")
        
        # Test parent instance creation
        self.assertIsInstance(parent, ParentClass)
        self.assertEqual(parent.parent_value, "custom_parent")
        
        # Test child instance creation and inheritance
        self.assertIsInstance(child, ChildClass)
        self.assertIsInstance(child, ParentClass)  # Should also be an instance of parent
        self.assertEqual(child.child_value, "custom_child")
        self.assertEqual(child.parent_value, "inherited_parent")
        
        # Debug output tests
        debug_dump(ParentClass)
        debug_dump(ChildClass)
        debug_dump(parent)
        debug_dump(child)
        exit()