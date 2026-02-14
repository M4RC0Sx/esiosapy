from __future__ import annotations

import logging
import time

from typing import Optional
from typing import Union
from urllib.parse import urljoin

import requests

from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from esiosapy.exceptions import APIResponseError
from esiosapy.exceptions import AuthenticationError
from esiosapy.exceptions import ESIOSAPIError


logger = logging.getLogger("esiosapy")


# Retry conditions: retry on network errors, but not on auth/server errors
retry_conditions = retry_if_exception_type(ESIOSAPIError)


class RequestHelper:
    """
    A helper class to manage HTTP requests, including adding default headers
    and making GET requests.

    This class simplifies the process of making HTTP GET requests by handling
    common tasks such as setting default headers and constructing the full URL.
    """

    def __init__(self, base_url: str, token: str, timeout: int = 30):
        """
        Initializes the RequestHelper with a base URL and an API token.

        :param base_url: The base URL for the API endpoints.
        :type base_url: str
        :param token: The API token used for authentication in requests.
        :type token: str
        :param timeout: Request timeout in seconds, defaults to 30.
        :type timeout: int
        """
        self.base_url = base_url
        self.token = token
        self.timeout = timeout
        self._session = requests.Session()

    def add_default_headers(self, headers: dict[str, str]) -> dict[str, str]:
        """
        Adds default headers to the provided headers dictionary.

        This method adds the 'Accept', 'Content-Type', and 'x-api-key' headers
        to the headers dictionary if they are not already present.

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

        return headers

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
        retry=(retry_conditions),
    )
    def get_request(
        self,
        path: str,
        headers: Optional[dict[str, str]] = None,
        params: Optional[dict[str, Union[str, int, list[str]]]] = None,
    ) -> requests.Response:
        """
        Makes a GET request to the specified path, with optional headers and parameters.

        This method constructs the full URL by combining the base URL and the
        provided path. It then sends a GET request to this URL, including any
        provided headers and query parameters.

        :param path: The endpoint path to be appended to the base URL.
        :type path: str
        :param headers: Optional headers to include in the request. If not provided,
                        default headers will be added. Defaults to None.
        :type headers: Optional[Dict[str, str]], optional
        :param params: Optional query parameters to include in the request. This can
                       include strings, integers, or lists of strings. Defaults to None.
        :type params: Optional[Dict[str, Union[str, int, List[str]]]], optional
        :return: The response object resulting from the GET request.
        :rtype: requests.Response
        """
        if headers is None:
            headers = {}
        if params is None:
            params = {}

        headers = self.add_default_headers(headers)
        url = urljoin(self.base_url, path)

        start_time = time.monotonic()
        logger.debug(
            "HTTP request",
            extra={"method": "GET", "url": url, "params": params},
        )

        try:
            response = self._session.get(
                url, headers=headers, params=params, timeout=self.timeout
            )
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
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response else None
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
            raise APIResponseError(msg, status_code=status_code) from e
        except requests.RequestException as e:
            logger.error(
                "Network error",
                extra={"method": "GET", "url": url, "error": str(e)},
            )
            msg = f"Network error: {e}"
            raise ESIOSAPIError(msg) from e

        return response
