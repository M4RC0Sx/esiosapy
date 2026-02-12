from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Optional
from typing import Union

from esiosapy.models.indicator.indicator import Indicator


if TYPE_CHECKING:
    from esiosapy.utils.async_request_helper import AsyncRequestHelper


class AsyncIndicatorManager:
    """
    Manages indicator-related operations for the ESIOS API (async version).

    This class provides methods to retrieve and search for indicators from the
    ESIOS API, including listing all available indicators and searching for
    indicators by name.
    """

    _endpoint = "/indicators"

    def __init__(self, request_helper: AsyncRequestHelper) -> None:
        """
        Initializes the AsyncIndicatorManager with an AsyncRequestHelper.

        :param request_helper: An instance of AsyncRequestHelper used to make API requests.
        :type request_helper: AsyncRequestHelper
        """
        self.request_helper = request_helper

    def _init_indicator(self, data: dict[str, Union[str, int]]) -> Indicator:
        """
        Initializes an Indicator object from a dictionary of indicator data.

        :param data: A dictionary containing indicator data.
        :type data: Dict[str, Union[str, int]]
        :return: An Indicator object initialized with the provided data.
        :rtype: Indicator
        """
        return Indicator(**data, raw=data, _request_helper=self.request_helper)

    async def list_all(
        self, taxonomy_terms: Optional[list[str]] = None
    ) -> list[Indicator]:
        """
        Retrieves a list of all indicators, optionally.

        This method filtered by taxonomy terms sends a GET request to the `/indicators` endpoint and
        returns a list of Indicator objects.

        :param taxonomy_terms: A list of taxonomy terms to filter the indicators,
                               defaults to None.
        :type taxonomy_terms: Optional[List[str]], optional
        :return: A list of Indicator objects representing all (or filtered) indicators.
        :rtype: List[Indicator]
        """
        params: dict[str, Union[str, int, list[str]]] = {}
        if taxonomy_terms:
            params["taxonomy_terms[]"] = taxonomy_terms

        response = await self.request_helper.get_request(self._endpoint, params=params)
        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]

    async def search(self, name: str) -> list[Indicator]:
        """
        Searches for indicators by name.

        This method sends a GET request to the `/indicators` endpoint with a
        search query, returning a list of Indicator objects.

        :param name: The name or part of the name to search for in indicators.
        :type name: str
        :return: A list of Indicator objects that match the search query.
        :rtype: List[Indicator]
        """
        response = await self.request_helper.get_request(
            self._endpoint, params={"text": name}
        )
        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]
