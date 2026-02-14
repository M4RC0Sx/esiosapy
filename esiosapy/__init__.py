"""esiosapy - Unofficial ESIOS API Python library."""

from __future__ import annotations


__version__ = "2.2.3"
__author__ = "M4RC0Sx"

from esiosapy.async_client import AsyncESIOSAPYClient
from esiosapy.client import ESIOSAPYClient
from esiosapy.constants import ESIOS_API_URL
from esiosapy.exceptions import APIResponseError
from esiosapy.exceptions import AuthenticationError
from esiosapy.exceptions import ESIOSAPIError
from esiosapy.managers.archive_manager import ArchiveManager
from esiosapy.managers.async_archive_manager import AsyncArchiveManager
from esiosapy.managers.async_indicator_manager import AsyncIndicatorManager
from esiosapy.managers.async_offer_indicator_manager import AsyncOfferIndicatorManager
from esiosapy.managers.indicator_manager import IndicatorManager
from esiosapy.managers.offer_indicator_manager import OfferIndicatorManager


__all__ = [
    "ESIOS_API_URL",
    "APIResponseError",
    "ArchiveManager",
    "AsyncArchiveManager",
    "AsyncESIOSAPYClient",
    "AsyncIndicatorManager",
    "AsyncOfferIndicatorManager",
    "AuthenticationError",
    "ESIOSAPIError",
    "ESIOSAPYClient",
    "IndicatorManager",
    "OfferIndicatorManager",
    "__author__",
    "__version__",
]
