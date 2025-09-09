from abc import ABC
from typing import Any, Optional, Callable

from attrs import field

from wexample_helpers.enums.field_visibility import FieldVisibility


class BaseField(ABC):
    """Base class for all field types."""

    def __init__(self, description: str, validator: Callable = None, default: Any = None, **kwargs):
        self.description = description
        self.validator = validator
        self.default = default
        self.extra_kwargs = kwargs

    @property
    def visibility(self) -> FieldVisibility:
        return FieldVisibility.PUBLIC  # Override in subclasses

    def to_attrs_field(self) -> Any:
        """Convert to attrs field with proper metadata and validation."""
        # Separate attrs parameters from metadata
        attrs_params = ['init', 'repr', 'eq', 'order', 'hash', 'compare', 'kw_only', 'on_setattr', 'alias', 'type']
        
        metadata = {
            'description': self.description,
            'visibility': self.visibility.value,
            'field_type': self.__class__.__name__
        }
        
        # Build field_kwargs with attrs parameters
        field_kwargs = {'metadata': metadata}
        
        # Extract attrs-specific parameters from extra_kwargs
        for param in attrs_params:
            if param in self.extra_kwargs:
                field_kwargs[param] = self.extra_kwargs[param]
        
        # Add remaining extra_kwargs to metadata
        remaining_kwargs = {k: v for k, v in self.extra_kwargs.items() if k not in attrs_params}
        metadata.update(remaining_kwargs)

        # Combine name validation + custom validation
        validators = self._build_validators()

        if self.default is not None:
            field_kwargs['default'] = self.default
        if validators:
            field_kwargs['validator'] = validators

        return field(**field_kwargs)

    def _build_validators(self) -> Optional[Callable]:
        """Build combined validator function."""
        name_validator = self._create_name_validator()
        custom_validator = self.validator

        if not name_validator and not custom_validator:
            return None

        def combined_validator(instance, attribute, value):
            # Check naming convention first
            if name_validator:
                name_validator(instance, attribute, value)

            # Then custom validation
            if custom_validator:
                custom_validator(instance, attribute, value)

            return value

        return combined_validator

    def _create_name_validator(self) -> Optional[Callable]:
        """Create validator for field name conventions."""
        expected_prefix = self._get_expected_prefix()
        if not expected_prefix:
            return None

        def name_validator(instance, attribute, value):
            if not attribute.name.startswith(expected_prefix):
                raise ValueError(
                    f"{self.__class__.__name__} '{attribute.name}' must start with "
                    f"'{expected_prefix}' (current: {self.visibility.value})"
                )

        return name_validator

    def _get_expected_prefix(self) -> Optional[str]:
        """Get expected prefix based on visibility."""
        if self.visibility in [FieldVisibility.PRIVATE, FieldVisibility.PROTECTED]:
            return '_'
        return None
