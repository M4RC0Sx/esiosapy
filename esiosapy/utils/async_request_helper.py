from __future__ import annotations

import logging
import time

from typing import Any
from typing import Optional

from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from esiosapy import __version__
from esiosapy.exceptions import APIResponseError
from esiosapy.exceptions import AuthenticationError
from esiosapy.exceptions import ESIOSAPIError


logger = logging.getLogger("esiosapy")


try:
    import httpx

    _HTTPX_AVAILABLE = True
except ImportError:
    _HTTPX_AVAILABLE = False

# Retry conditions: retry on network errors, but not on auth/server errors
retry_conditions = retry_if_exception_type(ESIOSAPIError)


class AsyncRequestHelper:
    """
    Async helper class to manage HTTP requests, including adding default headers
    and making GET requests.

    This class uses httpx for async HTTP operations, providing better performance
    for concurrent API calls.

    Requires httpx to be installed. Install with: pip install esiosapy[async]
    """

    def __init__(self, base_url: str, token: str, timeout: int = 30) -> None:
        """
        Initializes the AsyncRequestHelper with a base URL and an API token.

        :param base_url: The base URL for the API endpoints.
        :type base_url: str
        :param token: The API token used for authentication in requests.
        :type token: str
        :param timeout: Request timeout in seconds, defaults to 30.
        :type timeout: int
        :raises ImportError: If httpx is not installed.
        """
        if not _HTTPX_AVAILABLE:
            raise ImportError(
                "The `httpx` package is required to prettify the description. "
                "Install it with 'pip install httpx' "
                "or with your preferred package manager."
            )
        self.base_url = base_url
        self.token = token
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    def _get_client(self) -> httpx.AsyncClient:
        """Get or create the async client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def close(self) -> None:
        """Close the async client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> AsyncRequestHelper:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    def add_default_headers(self, headers: dict[str, str]) -> dict[str, str]:
        """
        Adds default headers to the provided headers dictionary.

        :param headers: The headers to which the defaults will be added.
        :type headers: Dict[str, str]
        :return: The updated headers dictionary with default headers added.
        :rtype: Dict[str, str]
        """
        if "Accept" not in headers:
            headers["Accept"] = "application/json; application/vnd.esios-api-v1+json"

        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

        if "x-api-key" not in headers:
            headers["x-api-key"] = self.token

        if "User-Agent" not in headers:
            headers["User-Agent"] = f"esiosapy/{__version__}"

        return headers

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
        retry=retry_conditions,
    )
    async def get_request(
        self,
        path: str,
        headers: Optional[dict[str, str]] = None,
        params: Optional[Any] = None,
    ) -> httpx.Response:
        """
        Makes an async GET request to the specified path.

        :param path: The endpoint path to be appended to the base URL.
        :type path: str
        :param headers: Optional headers to include in the request.
        :type headers: Optional[Dict[str, str]], optional
        :param params: Optional query parameters to include in the request.
        :type params: Optional[Any], optional
        :return: The response object resulting from the GET request.
        :rtype: httpx.Response
        """
        if headers is None:
            headers = {}
        if params is None:
            params = {}

        headers = self.add_default_headers(headers)
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

        client = self._get_client()

        start_time = time.monotonic()
        logger.debug(
            "HTTP request",
            extra={"method": "GET", "url": url, "params": params},
        )

        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            elapsed = time.monotonic() - start_time
            logger.debug(
                "HTTP response",
                extra={
                    "method": "GET",
                    "url": url,
                    "status": response.status_code,
                    "elapsed": f"{elapsed:.3f}s",
                },
            )
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            logger.error(
                "HTTP error",
                extra={
                    "method": "GET",
                    "url": url,
                    "status": status_code,
                    "error": str(e),
                },
            )
            if status_code == 401:
                msg = "Authentication failed. Check your API token."
                raise AuthenticationError(msg, {"status_code": status_code}) from e
            if status_code == 403:
                msg = "Access forbidden. Check your API token permissions."
                raise AuthenticationError(msg, {"status_code": status_code}) from e
            msg = f"API request failed with status {status_code}"
            raise APIResponseError(
                msg, status_code=status_code, response_body=str(e.response.content)
            ) from e
        except httpx.RequestError as e:
            logger.error(
                "Network error",
                extra={"method": "GET", "url": url, "error": str(e)},
            )
            msg = f"Network error: {e}"
            raise ESIOSAPIError(msg) from e

        return response
