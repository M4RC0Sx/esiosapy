from typing import Dict, List, Optional, Union
from urllib.parse import urljoin

import requests


class RequestHelper:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

    def add_default_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
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
        if headers is None:
            headers = {}
        if params is None:
            params = {}

        headers = self.add_default_headers(headers)
        url = urljoin(self.base_url, path)

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response
