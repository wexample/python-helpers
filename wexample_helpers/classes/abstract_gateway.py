import requests
import time
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from wexample_helpers.const.types import StringsList
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import HasSnakeShortClassNameClassMixin
from wexample_helpers.errors.gateway_authentication_error import GatewayAuthenticationError
from wexample_helpers.errors.gateway_error import GatewayError
from wexample_helpers.errors.gateway_connexion_error import GatewayConnectionError


class AbstractGateway(HasSnakeShortClassNameClassMixin, BaseModel):
    # Base configuration
    base_url: str = Field(..., description="Base API URL")
    api_keys: Dict[str, str] = Field(default=None, description="Required API keys")
    timeout: int = Field(default=30, description="Request timeout in seconds")

    # State
    connected: bool = Field(default=False, description="Connection state")
    last_request_time: Optional[float] = Field(default=None, description="Timestamp of last request")
    rate_limit_delay: float = Field(default=1.0, description="Minimum delay between requests in seconds")

    # Default request configuration
    default_headers: Dict[str, str] = Field(default=None, description="Default headers for requests")

    def model_post_init(self, *args, **kwargs):
        super().model_post_init(*args, **kwargs)
        if self.api_keys is None:
            self.api_keys = {}
        if self.default_headers is None:
            self.default_headers = {}

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_class_name_suffix(cls) -> Optional[str]:
        return 'GatewayService'

    def connect(self) -> bool:
        """
        Establishes connection with the API.
        Verifies that all required API keys are present.
        """
        required_keys = self.get_expected_env_keys()
        missing_keys = [key for key in required_keys if key not in self.api_keys]

        if missing_keys:
            raise GatewayAuthenticationError(f"Missing required API keys: {', '.join(missing_keys)}")

        if self.check_connection():
            self.connected = True
            return True

        raise GatewayConnectionError("Failed to connect to the API")

    def check_connection(self) -> bool:
        """
        Checks if the API is accessible.
        Should be overridden in child classes for specific verification.
        """
        try:
            return self._check_url(self.base_url)
        except Exception as e:
            return False

    def get_expected_env_keys(self) -> StringsList:
        """
        Returns the list of required API keys.
        Should be overridden in child classes.
        """
        return []

    def _check_url(self, url: str) -> bool:
        """
        Checks if a URL is accessible.
        """
        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                headers=self.default_headers
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def _handle_rate_limiting(self):
        """
        Handles basic rate limiting.
        """
        if self.last_request_time is not None:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.rate_limit_delay:
                time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    async def make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Utility method to make HTTP requests.
        """
        if not self.connected:
            raise GatewayConnectionError("Gateway is not connected")

        self._handle_rate_limiting()

        full_url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        request_headers = {**self.default_headers, **(headers or {})}

        try:
            response = requests.request(
                method=method,
                url=full_url,
                json=data,
                params=params,
                headers=request_headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise GatewayError(f"Request failed: {str(e)}")

    def set_api_key(self, key_name: str, key_value: str):
        """
        Sets an API key.
        """
        self.api_keys[key_name] = key_value

    def get_api_key(self, key_name: str) -> str:
        """
        Retrieves an API key.
        """
        if key_name not in self.api_keys:
            raise GatewayAuthenticationError(f"API key '{key_name}' not found")
        return self.api_keys[key_name]
