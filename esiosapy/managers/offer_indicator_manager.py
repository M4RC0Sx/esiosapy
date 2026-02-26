from __future__ import annotations

from typing import TYPE_CHECKING

from esiosapy.managers.base import BaseOfferIndicatorManager
from esiosapy.utils.request_helper import RequestHelper


if TYPE_CHECKING:
    from esiosapy.models.offer_indicator.offer_indicator import OfferIndicator


class OfferIndicatorManager(BaseOfferIndicatorManager[RequestHelper]):
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
        """
        super().__init__(request_helper)

    def list_all(self, taxonomy_terms: list[str] | None = None) -> list[OfferIndicator]:
        """
        Retrieves a list of all offer indicators, optionally filtered by taxonomy terms.

        This method sends a GET request to the `/offer_indicators` endpoint and
        returns a list of OfferIndicator objects. If taxonomy terms are provided,
        they are used to filter the offer indicators.

        :param taxonomy_terms: A list of taxonomy terms to filter the offer indicators,
                               defaults to None.
        :return: A list of OfferIndicator objects representing all (or filtered)
                 offer indicators.
        """
        params: dict[str, str | int | list[str]] = {}
        if taxonomy_terms:
            params["taxonomy_terms[]"] = taxonomy_terms

        response = self.request_helper.get_request(self._endpoint, params=params)

        return [
            self._init_indicator(indicator)
            for indicator in response.json()["indicators"]
        ]
