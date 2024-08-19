from typing import Dict, List, Optional, Union

from esiosapy.models.indicator.indicator import Indicator
from esiosapy.utils.request_helper import RequestHelper


class IndicatorManager:
    def __init__(self, request_helper: RequestHelper) -> None:
        self.request_helper = request_helper

    def _init_indicator(self, indicator: Dict[str, Union[str, int]]) -> Indicator:
        return Indicator(
            **indicator, raw=indicator, _request_helper=self.request_helper
        )

    def list_all(self, taxonomy_terms: Optional[List[str]] = None) -> List[Indicator]:
        params: Dict[str, Union[str, int, List[str]]] = {}
        if taxonomy_terms:
            params["taxonomy_terms[]"] = taxonomy_terms

        response = self.request_helper.get_request("/indicators", params=params)
        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]

    def search(self, name: str) -> List[Indicator]:
        response = self.request_helper.get_request("/indicators", params={"text": name})
        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]
