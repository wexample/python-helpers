import requests
import time
import os
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
    timeout: int = Field(default=30, description="Request timeout in seconds")

    # State
    connected: bool = Field(default=False, description="Connection state")
    last_request_time: Optional[float] = Field(default=None, description="Timestamp of last request")
    rate_limit_delay: float = Field(default=1.0, description="Minimum delay between requests in seconds")

    # Default request configuration
    default_headers: Dict[str, str] = Field(default=None, description="Default headers for requests")

    def model_post_init(self, *args, **kwargs):
        super().model_post_init(*args, **kwargs)
        if self.default_headers is None:
            self.default_headers = {}

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_class_name_suffix(cls) -> Optional[str]:
        return 'GatewayService'

    def connect(self) -> bool:
        required_keys = self.get_expected_env_keys()
        missing_keys = [key for key in required_keys if not os.getenv(key)]

        if missing_keys:
            raise GatewayAuthenticationError(f"Missing required environment variables: {', '.join(missing_keys)}")

        if self.check_connection():
            self.connected = True
            return True

        raise GatewayConnectionError("Failed to connect to the API")

    def check_connection(self) -> bool:
        try:
            return self._check_url(self.base_url)
        except Exception as e:
            return False

    def get_expected_env_keys(self) -> StringsList:
        return []

    def _check_url(self, url: str) -> bool:
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
        if self.last_request_time is not None:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.rate_limit_delay:
                time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    def make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
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
