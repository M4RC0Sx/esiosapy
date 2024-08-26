from typing import Dict, List, Optional, Union

from esiosapy.models.indicator.indicator import Indicator
from esiosapy.utils.request_helper import RequestHelper


class IndicatorManager:
    """
    Manages indicator-related operations for the ESIOS API.

    This class provides methods to retrieve and search for indicators from the
    ESIOS API, including listing all available indicators and searching for
    indicators by name.
    """

    def __init__(self, request_helper: RequestHelper) -> None:
        """
        Initializes the IndicatorManager with a RequestHelper.

        :param request_helper: An instance of RequestHelper used to make API requests.
        :type request_helper: RequestHelper
        """
        self.request_helper = request_helper

    def _init_indicator(self, indicator: Dict[str, Union[str, int]]) -> Indicator:
        """
        Initializes an Indicator object from a dictionary of indicator data.

        :param indicator: A dictionary containing indicator data.
        :type indicator: Dict[str, Union[str, int]]
        :return: An Indicator object initialized with the provided data.
        :rtype: Indicator
        """
        return Indicator(
            **indicator, raw=indicator, _request_helper=self.request_helper
        )

    def list_all(self, taxonomy_terms: Optional[List[str]] = None) -> List[Indicator]:
        """
        Retrieves a list of all indicators, optionally filtered by taxonomy terms.

        This method sends a GET request to the `/indicators` endpoint and
        returns a list of Indicator objects. If taxonomy terms are provided,
        they are used to filter the indicators.

        :param taxonomy_terms: A list of taxonomy terms to filter the indicators,
                               defaults to None.
        :type taxonomy_terms: Optional[List[str]], optional
        :return: A list of Indicator objects representing all (or filtered) indicators.
        :rtype: List[Indicator]
        """
        params: Dict[str, Union[str, int, List[str]]] = {}
        if taxonomy_terms:
            params["taxonomy_terms[]"] = taxonomy_terms

        response = self.request_helper.get_request("/indicators", params=params)
        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]

    def search(self, name: str) -> List[Indicator]:
        """
        Searches for indicators by name.

        This method sends a GET request to the `/indicators` endpoint with a
        search query, returning a list of Indicator objects that match the
        specified name.

        :param name: The name or part of the name to search for in indicators.
        :type name: str
        :return: A list of Indicator objects that match the search query.
        :rtype: List[Indicator]
        """
        response = self.request_helper.get_request("/indicators", params={"text": name})
        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]
