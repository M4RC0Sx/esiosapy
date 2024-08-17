from typing import Dict
from urllib.parse import urljoin, urlparse

import requests

from esiosapy.managers.archive_manager import ArchiveManager
from esiosapy.managers.indicator_manager import IndicatorManager
from esiosapy.utils.request_helper import RequestHelper

ESIOS_API_URL = "https://api.esios.ree.es/"


class ESIOSAPYClient:
    def __init__(self, token: str, base_url: str = ESIOS_API_URL):
        self.token = token
        self.base_url = base_url
        self.request_helper = RequestHelper(base_url, token)

        self.archives: ArchiveManager = ArchiveManager(self.request_helper)
        self.indicators: IndicatorManager = IndicatorManager(self.request_helper)

    def raw_request(self, url: str, headers: Dict[str, str] = {}) -> requests.Response:
        headers = self.request_helper.add_default_headers(headers)

        if urlparse(url).netloc == "":
            url = urljoin(self.base_url, url)

        return requests.get(url, headers={"Accept": "application/json"})
