from typing import Dict, List, Optional, Union

from esiosapy.models.offer_indicator.offer_indicator import OfferIndicator
from esiosapy.utils.request_helper import RequestHelper


class OfferIndicatorManager:
    def __init__(self, request_helper: RequestHelper) -> None:
        self.request_helper = request_helper

    def _init_indicator(self, indicator: Dict[str, Union[str, int]]) -> OfferIndicator:
        return OfferIndicator(
            **indicator, raw=indicator, _request_helper=self.request_helper
        )

    def list_all(
        self, taxonomy_terms: Optional[List[str]] = None
    ) -> List[OfferIndicator]:
        params: Dict[str, Union[str, int, List[str]]] = {}
        if taxonomy_terms:
            params["taxonomy_terms[]"] = taxonomy_terms

        response = self.request_helper.get_request("/offer_indicators", params=params)

        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]
