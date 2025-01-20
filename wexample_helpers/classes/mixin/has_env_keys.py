from typing import List, Mapping


class HasEnvKeys:
    """Mixin class to handle environment variables validation."""

    def model_post_init(self, *args, **kwargs):
        """
        Validate environment variables right after initialization.
        This method is called by Pydantic after the model is initialized.
        """
        super().model_post_init(*args, **kwargs)
        self.validate_env_keys()

    def get_expected_env_keys(self) -> List[str]:
        """
        Returns a list of required environment variable keys.
        Should be overridden by child classes.
        """
        return []

    def validate_env_keys(self) -> None:
        """
        Validates that all required environment variables are set.
        Raises MissingRequiredEnvVarError if any required variable is missing.
        """
        required_keys = self.get_expected_env_keys()
        env_registry = self._get_env_registry()
        missing_keys = [key for key in required_keys if not env_registry.get(key)]

        if missing_keys:
            from wexample_helpers.errors.missing_required_env_var_error import MissingRequiredEnvVarError

            raise MissingRequiredEnvVarError(missing_keys)

    def _get_env_registry(self) -> Mapping[str, str]:
        """
        Returns the environment registry to use for validation.
        Can be overridden by child classes to use a different registry.
        """
        import os
        return os.environ
