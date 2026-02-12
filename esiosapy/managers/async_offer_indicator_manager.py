from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Optional
from typing import Union

from esiosapy.models.offer_indicator.offer_indicator import OfferIndicator


if TYPE_CHECKING:
    from esiosapy.utils.async_request_helper import AsyncRequestHelper


class AsyncOfferIndicatorManager:
    """
    Manages offer indicator-related operations for the ESIOS API (async version).

    This class provides methods to retrieve offer indicators from the ESIOS API,
    including listing all available offer indicators with optional filtering by
    taxonomy terms.
    """

    _endpoint = "/offer_indicators"

    def __init__(self, request_helper: AsyncRequestHelper) -> None:
        """
        Initializes the AsyncOfferIndicatorManager with an AsyncRequestHelper.

        :param request_helper: An instance of AsyncRequestHelper used to make API requests.
        :type request_helper: AsyncRequestHelper
        """
        self.request_helper = request_helper

    def _init_indicator(self, data: dict[str, Union[str, int]]) -> OfferIndicator:
        """
        Initializes an OfferIndicator object from a dictionary of indicator data.

        :param data: A dictionary containing offer indicator data.
        :type data: Dict[str, Union[str, int]]
        :return: An OfferIndicator object initialized with the provided data.
        :rtype: OfferIndicator
        """
        return OfferIndicator(**data, raw=data, _request_helper=self.request_helper)

    async def list_all(
        self, taxonomy_terms: Optional[list[str]] = None
    ) -> list[OfferIndicator]:
        """
        Retrieves a list of all offer indicators, optionally filtered by taxonomy terms.

        This method sends a GET request to the `/offer_indicators` endpoint and
        returns a list of OfferIndicator objects.

        :param taxonomy_terms: A list of taxonomy terms to filter the offer indicators,
                               defaults to None.
        :type taxonomy_terms: Optional[List[str]], optional
        :return: A list of OfferIndicator objects representing all (or filtered)
                 offer indicators.
        :rtype: List[OfferIndicator]
        """
        params: dict[str, Union[str, int, list[str]]] = {}
        if taxonomy_terms:
            params["taxonomy_terms[]"] = taxonomy_terms

        response = await self.request_helper.get_request(self._endpoint, params=params)

        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]
