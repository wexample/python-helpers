from wexample_helpers.helpers.polyfill import polyfill_import


def test_register_global_types):
    # Test that the function accepts any type of argument without raising exceptions
    class DummyClass:
        pass

    # Test with various types of arguments
    register_global_typesDummyClass)
    register_global_types[DummyClass, str, int])
    register_global_typesNone)
    register_global_types42)
    register_global_types"string")
    
    # Test with multiple classes
    class Class1:
        pass
    
    class Class2:
        pass
    
    register_global_types[Class1, Class2])
    
    # The function should always return None
    assert register_global_typesDummyClass) is None
