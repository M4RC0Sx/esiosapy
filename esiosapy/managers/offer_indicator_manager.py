from typing import Dict, List, Optional, Union

from esiosapy.models.offer_indicator.offer_indicator import OfferIndicator
from esiosapy.utils.request_helper import RequestHelper


class OfferIndicatorManager:
    """
    Manages offer indicator-related operations for the ESIOS API.

    This class provides methods to retrieve offer indicators from the ESIOS API,
    including listing all available offer indicators with optional filtering by
    taxonomy terms.
    """

    def __init__(self, request_helper: RequestHelper) -> None:
        """
        Initializes the OfferIndicatorManager with a RequestHelper.

        :param request_helper: An instance of RequestHelper used to make API requests.
        :type request_helper: RequestHelper
        """
        self.request_helper = request_helper

    def _init_indicator(self, indicator: Dict[str, Union[str, int]]) -> OfferIndicator:
        """
        Initializes an OfferIndicator object from a dictionary of indicator data.

        :param indicator: A dictionary containing offer indicator data.
        :type indicator: Dict[str, Union[str, int]]
        :return: An OfferIndicator object initialized with the provided data.
        :rtype: OfferIndicator
        """
        return OfferIndicator(
            **indicator, raw=indicator, _request_helper=self.request_helper
        )

    def list_all(
        self, taxonomy_terms: Optional[List[str]] = None
    ) -> List[OfferIndicator]:
        """
        Retrieves a list of all offer indicators, optionally filtered by taxonomy terms.

        This method sends a GET request to the `/offer_indicators` endpoint and
        returns a list of OfferIndicator objects. If taxonomy terms are provided,
        they are used to filter the offer indicators.

        :param taxonomy_terms: A list of taxonomy terms to filter the offer indicators,
                               defaults to None.
        :type taxonomy_terms: Optional[List[str]], optional
        :return: A list of OfferIndicator objects representing all (or filtered)
                 offer indicators.
        :rtype: List[OfferIndicator]
        """
        params: Dict[str, Union[str, int, List[str]]] = {}
        if taxonomy_terms:
            params["taxonomy_terms[]"] = taxonomy_terms

        response = self.request_helper.get_request("/offer_indicators", params=params)

        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]
