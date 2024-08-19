from typing import Dict, List, Optional, Union
from urllib.parse import urljoin

import requests


class RequestHelper:
    """
    A helper class to manage HTTP requests, including adding default headers
    and making GET requests.

    This class simplifies the process of making HTTP GET requests by handling
    common tasks such as setting default headers and constructing the full URL.
    """

    def __init__(self, base_url: str, token: str):
        """
        Initializes the RequestHelper with a base URL and an API token.

        :param base_url: The base URL for the API endpoints.
        :type base_url: str
        :param token: The API token used for authentication in requests.
        :type token: str
        """
        self.base_url = base_url
        self.token = token

    def add_default_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
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

    def get_request(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Union[str, int, List[str]]]] = None,
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

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response
