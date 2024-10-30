from types import UnionType
from typing import Any, List, Dict, Tuple, Union, get_origin, get_args, Type
from typing import Any, Type, Union, get_origin, get_args


def type_is_generic(type_value: Any) -> bool:
    """Detects if a given type is a generic type like List, Dict, Union"""

    # Set of known generic types for quick membership testing
    generic_types = {list, dict, tuple, List, Dict, Tuple, Union}

    # Extract the base type of type_value using get_origin, or use type_value itself if get_origin is None
    type_value = get_origin(type_value) or type_value

    # Check if type_value is a known generic type
    return type_value in generic_types


def type_generic_value_is_valid(raw_value: Any, allowed_type: Type | UnionType) -> bool:
    """Helper to recursively validate parameter types for generics like Dict, List, Tuple, and Union."""
    origin = get_origin(allowed_type) or allowed_type
    args = get_args(allowed_type)

    # Validate Union type by checking if raw_value matches any of the types in the Union
    if origin is Union:
        return any(type_generic_value_is_valid(raw_value, arg) for arg in args)

    # Validate dictionary type with possible nested generics
    if origin is dict:
        if not isinstance(raw_value, dict):
            return False
        # Accept empty dict
        if not raw_value:
            return True
        # Validate key and value types recursively
        key_type, value_type = args if len(args) == 2 else (Any, Any)
        return all(type_generic_value_is_valid(k, key_type)
                   and type_generic_value_is_valid(v, value_type)
                   for k, v in raw_value.items())

    # Validate list type with possible nested generics
    elif origin is list:
        if not isinstance(raw_value, list):
            return False
        # Accept empty list
        if not raw_value:
            return True
        # Validate item type recursively
        item_type = args[0] if args else Any
        return all(type_generic_value_is_valid(item, item_type) for item in raw_value)

    # Validate tuple type with possible nested generics
    elif origin is tuple:
        if not isinstance(raw_value, tuple) or (args and len(raw_value) != len(args)):
            return False
        # Validate each item in the tuple recursively
        return all(type_generic_value_is_valid(item, arg) for item, arg in zip(raw_value, args) if args)
    elif origin is Any:
        return True

    # For any other types, fallback to isinstance check
    return isinstance(raw_value, origin)


def type_is_compatible(actual_type: Type, allowed_type: Type) -> bool:
    """Check if actual_type is compatible with allowed_type for generics like Dict, List, Tuple, and Union."""
    origin = get_origin(allowed_type) or allowed_type
    actual_origin = get_origin(actual_type) or actual_type
    allowed_args = get_args(allowed_type)
    actual_args = get_args(actual_type)

    # Case 1: If allowed_type is Any, it is compatible with any actual_type
    if origin is Any:
        return True

    # Case 2: Handle Union type for allowed_type
    if origin is Union:
        return any(type_is_compatible(actual_type, arg) for arg in allowed_args)

    # Case 3: Handle dictionary type with possible nested generics
    if origin is dict:
        if actual_origin is not dict:
            return False
        # Check compatibility for key and value types recursively
        key_type, value_type = allowed_args if len(allowed_args) == 2 else (Any, Any)
        actual_key_type, actual_value_type = actual_args if len(actual_args) == 2 else (Any, Any)
        return (type_is_compatible(actual_key_type, key_type) and
                type_is_compatible(actual_value_type, value_type))

    # Case 4: Handle list type with possible nested generics
    elif origin is list:
        if actual_origin is not list:
            return False
        # Validate item type recursively
        item_type = allowed_args[0] if allowed_args else Any
        actual_item_type = actual_args[0] if actual_args else Any
        return type_is_compatible(actual_item_type, item_type)

    # Case 5: Handle tuple type with possible nested generics
    elif origin is tuple:
        if actual_origin is not tuple or len(actual_args) != len(allowed_args):
            return False
        # Validate each item type in the tuple recursively
        return all(type_is_compatible(act, exp) for act, exp in zip(actual_args, allowed_args))

    # Case 6: For other types, fall back to direct comparison
    return actual_type == allowed_type
