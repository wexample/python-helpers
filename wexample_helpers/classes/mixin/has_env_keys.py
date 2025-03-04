from typing import List, Any, Dict

from wexample_helpers.const.types import StringsList


class HasEnvKeys:
    """Mixin class to handle environment variables validation."""

    _env_values: Dict[str, str | None] = {}

    def get_expected_env_keys(self) -> List[str]:
        """
        Returns a list of required environment variable keys.
        Should be overridden by child classes.
        """
        return []

    def _load_env_file(self, file_path: str) -> None:
        from dotenv import load_dotenv, dotenv_values
        
        load_dotenv(file_path)
        self._env_values = dotenv_values(file_path)
        self._validate_env_keys()

    def _get_dotenv_file_name(self) -> str:
        from wexample_helpers.const.globals import FILE_NAME_ENV
        return FILE_NAME_ENV

    def _validate_env_keys(self) -> None:
        """
        Validates that all required environment variables are set.
        Raises MissingRequiredEnvVarError if any required variable is missing.
        """
        missing_keys = self._get_missing_env_keys(
            self.get_expected_env_keys()
        )

        if missing_keys:
            from wexample_helpers.errors.missing_required_env_var_error import MissingRequiredEnvVarError

            raise MissingRequiredEnvVarError(missing_keys)

    def _get_missing_env_keys(self, required_keys: StringsList) -> StringsList:
        import os

        missing = []
        for key in required_keys:
            if not os.environ.get(key) and key not in self._env_values:
                missing.append(key)
        return missing

    def get_env_parameter(self, key: str) -> Any:
        import os

        value = os.getenv(key)
        if value is None:
            value = self._env_values.get(key)
        if value is None:
            raise ValueError(f'Environment variable "{key}" is not defined.')
        return value