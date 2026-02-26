from __future__ import annotations

from typing import Any
from urllib.parse import urljoin
from urllib.parse import urlparse

from esiosapy.constants import ESIOS_API_URL
from esiosapy.managers.async_archive_manager import AsyncArchiveManager
from esiosapy.managers.async_indicator_manager import AsyncIndicatorManager
from esiosapy.managers.async_offer_indicator_manager import AsyncOfferIndicatorManager
from esiosapy.utils.async_request_helper import AsyncRequestHelper


try:
    import httpx  # noqa: TC002

    _HTTPX_AVAILABLE = True
except ImportError:
    _HTTPX_AVAILABLE = False


class AsyncESIOSAPYClient:
    """
    An async client for interacting with the ESIOS API.

    This client provides access to various managers that handle specific
    types of requests to the ESIOS API, such as archives, indicators, and
    offer indicators. It uses httpx for async HTTP operations.

    Requires httpx to be installed. Install with: pip install esiosapy[async]
    """

    def __init__(
        self,
        token: str,
        base_url: str = ESIOS_API_URL,
        timeout: int = 30,
    ) -> None:
        """
        Initializes the AsyncESIOSAPYClient with an API token and a base URL.

        :param token: The API token used for authentication.
        :type token: str
        :param base_url: The base URL for the ESIOS API. Defaults to ESIOS_API_URL.
        :type base_url: str, optional
        :param timeout: Request timeout in seconds, defaults to 30.
        :type timeout: int
        :raises ImportError: If httpx is not installed.
        """
        if not _HTTPX_AVAILABLE:
            raise ImportError(
                "The `httpx` package is required to use AsyncESIOSAPYClient. "
                "Install it with 'pip install httpx' "
                "or with your preferred package manager."
            )
        self.token = token
        self.base_url = base_url
        self.request_helper = AsyncRequestHelper(base_url, token, timeout)

        self.archives: AsyncArchiveManager = AsyncArchiveManager(self.request_helper)
        self.indicators: AsyncIndicatorManager = AsyncIndicatorManager(
            self.request_helper
        )
        self.offer_indicators: AsyncOfferIndicatorManager = AsyncOfferIndicatorManager(
            self.request_helper
        )

    async def close(self) -> None:
        """Close the async client and release resources."""
        await self.request_helper.close()

    async def __aenter__(self) -> AsyncESIOSAPYClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def raw_request(
        self,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """
        Makes a raw async GET request to a specified URL with optional headers.

        This method allows for making a direct GET request to a specified URL.
        It adds default headers to the request and handles URL construction
        if the provided URL is relative.

        :param url: The URL to which the GET request is made. If the URL is
                    relative, it will be joined with the base URL.
        :type url: str
        :param headers: Optional headers to include in the request. Defaults to None.
        :type headers: Optional[Dict[str, str]], optional
        :return: The response object resulting from the GET request.
        :rtype: httpx.Response
        """
        if headers is None:
            headers = {}
        headers = self.request_helper.add_default_headers(headers)

        if urlparse(url).netloc == "":
            url = urljoin(self.base_url, url)

        client = self.request_helper._get_client()
        response = await client.get(
            url, headers=headers, timeout=self.request_helper.timeout
        )
        return response
