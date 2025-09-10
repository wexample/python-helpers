from abc import ABC
from typing import Any, Optional, Callable

import attrs
from attrs import field

from wexample_helpers.enums.field_visibility import FieldVisibility


class BaseField(ABC):
    """Base class for all field types."""

    def __init__(
        self,
        description: str,
        validator: Optional[Callable] = None,
        default: Any = attrs.NOTHING,
        **kwargs
    ):
        self.description = description
        self.validator = validator
        self.default = default
        self.extra_kwargs = kwargs

    @property
    def visibility(self) -> FieldVisibility:
        return FieldVisibility.PUBLIC  # Override in subclasses

    def to_attrs_field(self) -> Any:
        """Convert to attrs field with proper metadata and validation."""
        attrs_params = [
            "init", "repr", "eq", "order", "hash", "compare",
            "kw_only", "on_setattr", "alias", "type", "factory"
        ]

        metadata = {
            "description": self.description,
            "visibility": self.visibility.value,
            "field_type": self.__class__.__name__,
        }

        field_kwargs = {"metadata": metadata}

        # seulement si un default explicite est fourni
        if self.default is not attrs.NOTHING:
            field_kwargs["default"] = self.default

        # attrs-specific kwargs
        for param in attrs_params:
            if param in self.extra_kwargs:
                field_kwargs[param] = self.extra_kwargs[param]

        # Les kwargs restants → metadata
        remaining_kwargs = {k: v for k, v in self.extra_kwargs.items() if k not in attrs_params}
        metadata.update(remaining_kwargs)

        # Validators
        validators = self._build_validators()
        if validators:
            field_kwargs["validator"] = validators

        return field(**field_kwargs)

    def _build_validators(self) -> Optional[Callable]:
        """Build combined validator function."""
        name_validator = self._create_name_validator()
        custom_validator = self.validator

        if not name_validator and not custom_validator:
            return None

        def combined_validator(instance, attribute, value):
            if name_validator:
                name_validator(instance, attribute, value)
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
            return "_"
        return None
