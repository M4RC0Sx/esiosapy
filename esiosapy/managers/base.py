from __future__ import annotations

from typing import Any
from typing import Generic
from typing import Protocol
from typing import TypeVar

from esiosapy.models.archive.archive import Archive
from esiosapy.models.indicator.indicator import Indicator
from esiosapy.models.offer_indicator.offer_indicator import OfferIndicator


class RequestHelperProtocol(Protocol):
    """Protocol defining the interface for request helpers."""

    base_url: str
    token: str

    def add_default_headers(self, headers: dict[str, str]) -> dict[str, str]: ...

    def get_request(
        self,
        path: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any: ...


# TypeVar bound to the protocol - allows same class to work with sync or async
RH = TypeVar("RH", bound="RequestHelperProtocol")


class BaseIndicatorManager(Generic[RH]):
    """
    Base class for indicator managers.

    This class provides common functionality for both sync and async
    indicator managers, reducing code duplication.
    """

    _endpoint = "/indicators"

    def __init__(self, request_helper: RH) -> None:
        """
        Initializes the manager with a request helper.

        :param request_helper: An instance of RequestHelper or AsyncRequestHelper.
        """
        self.request_helper = request_helper

    def _init_indicator(self, data: dict[str, Any]) -> Indicator:
        """
        Initializes an Indicator object from a dictionary of indicator data.

        :param data: A dictionary containing indicator data.
        :return: An Indicator object initialized with the provided data.
        """
        return Indicator(**data, raw=data, _request_helper=self.request_helper)


class BaseArchiveManager(Generic[RH]):
    """
    Base class for archive managers.

    This class provides common functionality for both sync and async
    archive managers, reducing code duplication.
    """

    _endpoint = "/archives"

    def __init__(self, request_helper: RH) -> None:
        """
        Initializes the manager with a request helper.

        :param request_helper: An instance of RequestHelper or AsyncRequestHelper.
        """
        self.request_helper = request_helper

    def _init_archive(self, data: dict[str, Any]) -> Archive:
        """
        Initializes an Archive object from a dictionary of archive data.

        :param data: A dictionary containing archive data.
        :return: An Archive object initialized with the provided data.
        """
        return Archive(**data, raw=data, _request_helper=self.request_helper)


class BaseOfferIndicatorManager(Generic[RH]):
    """
    Base class for offer indicator managers.

    This class provides common functionality for both sync and async
    offer indicator managers, reducing code duplication.
    """

    _endpoint = "/offer_indicators"

    def __init__(self, request_helper: RH) -> None:
        """
        Initializes the manager with a request helper.

        :param request_helper: An instance of RequestHelper or AsyncRequestHelper.
        """
        self.request_helper = request_helper

    def _init_indicator(self, data: dict[str, Any]) -> OfferIndicator:
        """
        Initializes an OfferIndicator object from a dictionary of indicator data.

        :param data: A dictionary containing offer indicator data.
        :return: An OfferIndicator object initialized with the provided data.
        """
        return OfferIndicator(**data, raw=data, _request_helper=self.request_helper)
