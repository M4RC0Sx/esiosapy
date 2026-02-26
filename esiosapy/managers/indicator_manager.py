from __future__ import annotations

from typing import TYPE_CHECKING

from esiosapy.managers.base import BaseIndicatorManager
from esiosapy.utils.request_helper import RequestHelper


if TYPE_CHECKING:
    from esiosapy.models.indicator.indicator import Indicator


class IndicatorManager(BaseIndicatorManager[RequestHelper]):
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
        """
        super().__init__(request_helper)

    def list_all(self, taxonomy_terms: list[str] | None = None) -> list[Indicator]:
        """
        Retrieves a list of all indicators, optionally filtered by taxonomy terms.

        This method sends a GET request to the `/indicators` endpoint and
        returns a list of Indicator objects. If taxonomy terms are provided,
        they are used to filter the indicators.

        :param taxonomy_terms: A list of taxonomy terms to filter the indicators,
                               defaults to None.
        :return: A list of Indicator objects representing all (or filtered) indicators.
        """
        params: dict[str, str | int | list[str]] = {}
        if taxonomy_terms:
            params["taxonomy_terms[]"] = taxonomy_terms

        response = self.request_helper.get_request(self._endpoint, params=params)
        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]

    def search(self, name: str) -> list[Indicator]:
        """
        Searches for indicators by name.

        This method sends a GET request to the `/indicators` endpoint with a
        search query, returning a list of Indicator objects that match the
        specified name.

        :param name: The name or part of the name to search for in indicators.
        :return: A list of Indicator objects that match the search query.
        """
        response = self.request_helper.get_request(
            self._endpoint, params={"text": name}
        )
        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]
