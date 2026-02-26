from __future__ import annotations

from typing import TYPE_CHECKING

from esiosapy.managers.base import BaseIndicatorManager
from esiosapy.utils.async_request_helper import AsyncRequestHelper


if TYPE_CHECKING:
    from esiosapy.models.indicator.indicator import Indicator


class AsyncIndicatorManager(BaseIndicatorManager[AsyncRequestHelper]):
    """
    Manages indicator-related operations for the ESIOS API (async version).

    This class provides methods to retrieve and search for indicators from the
    ESIOS API, including listing all available indicators and searching for
    indicators by name.
    """

    def __init__(self, request_helper: AsyncRequestHelper) -> None:
        """
        Initializes the AsyncIndicatorManager with an AsyncRequestHelper.

        :param request_helper: An instance of AsyncRequestHelper used to make API requests.
        """
        super().__init__(request_helper)

    async def list_all(
        self, taxonomy_terms: list[str] | None = None
    ) -> list[Indicator]:
        """
        Retrieves a list of all indicators, optionally filtered by taxonomy terms.

        This method sends a GET request to the `/indicators` endpoint and
        returns a list of Indicator objects.

        :param taxonomy_terms: A list of taxonomy terms to filter the indicators,
                               defaults to None.
        :return: A list of Indicator objects representing all (or filtered) indicators.
        """
        params: dict[str, str | int | list[str]] = {}
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
        :return: A list of Indicator objects that match the search query.
        """
        response = await self.request_helper.get_request(
            self._endpoint, params={"text": name}
        )
        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]
