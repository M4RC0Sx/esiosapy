from typing import Dict, Optional
from urllib.parse import urljoin, urlparse

import requests

from esiosapy.managers.archive_manager import ArchiveManager
from esiosapy.managers.indicator_manager import IndicatorManager
from esiosapy.managers.offer_indicator_manager import OfferIndicatorManager
from esiosapy.utils.request_helper import RequestHelper

ESIOS_API_URL = "https://api.esios.ree.es/"


class ESIOSAPYClient:
    """
    A client for interacting with the ESIOS API.

    This client provides access to various managers that handle specific
    types of requests to the ESIOS API, such as archives, indicators, and
    offer indicators. It simplifies the process of making requests by
    managing authentication and constructing the necessary URLs.
    """

    def __init__(self, token: str, base_url: str = ESIOS_API_URL):
        """
        Initializes the ESIOSAPYClient with an API token and a base URL.

        :param token: The API token used for authentication.
        :type token: str
        :param base_url: The base URL for the ESIOS API. Defaults to ESIOS_API_URL.
        :type base_url: str, optional
        """
        self.token = token
        self.base_url = base_url
        self.request_helper = RequestHelper(base_url, token)

        self.archives: ArchiveManager = ArchiveManager(self.request_helper)
        self.indicators: IndicatorManager = IndicatorManager(self.request_helper)
        self.offer_indicators: OfferIndicatorManager = OfferIndicatorManager(
            self.request_helper
        )

    def raw_request(
        self, url: str, headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Makes a raw GET request to a specified URL with optional headers.

        This method allows for making a direct GET request to a specified URL.
        It adds default headers to the request and handles URL construction
        if the provided URL is relative.

        :param url: The URL to which the GET request is made. If the URL is
                    relative, it will be joined with the base URL.
        :type url: str
        :param headers: Optional headers to include in the request. If not provided,
                        default headers will be added. Defaults to None.
        :type headers: Optional[Dict[str, str]], optional
        :return: The response object resulting from the GET request.
        :rtype: requests.Response
        """
        if headers is None:
            headers = {}
        headers = self.request_helper.add_default_headers(headers)

        if urlparse(url).netloc == "":
            url = urljoin(self.base_url, url)

        return requests.get(url, headers=headers)
