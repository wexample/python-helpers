import os
from wexample_helpers.const.types import StringsList
from wexample_helpers.errors.gateway_authentication_error import GatewayAuthenticationError


class HasEnvKeys:
    """Mixin class to handle environment variables validation."""

    def model_post_init(self, *args, **kwargs):
        """
        Validate environment variables right after initialization.
        This method is called by pydantic after the model is initialized.
        """
        super().model_post_init(*args, **kwargs)
        try:
            self.validate_env_keys()
        except GatewayAuthenticationError as e:
            self.io_manager.error(
                str(e),
                params={"class": self.__class__.__name__},
                fatal=True
            )
            raise

    def get_expected_env_keys(self) -> StringsList:
        """
        Returns a list of required environment variable keys.
        Should be overridden by child classes.
        """
        return []

    def validate_env_keys(self) -> None:
        """
        Validates that all required environment variables are set.
        Raises GatewayAuthenticationError if any required variable is missing.
        """
        required_keys = self.get_expected_env_keys()
        missing_keys = [key for key in required_keys if not os.getenv(key)]

        if missing_keys:
            error_message = f"Missing required environment variables: {', '.join(missing_keys)}"
            raise GatewayAuthenticationError(error_message)
