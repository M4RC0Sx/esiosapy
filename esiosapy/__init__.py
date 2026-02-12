"""esiosapy - Unofficial ESIOS API Python library."""

from __future__ import annotations


__version__ = "0.0.1"
__author__ = "M4RC0Sx"

from esiosapy.client import ESIOSAPYClient
from esiosapy.exceptions import APIResponseError
from esiosapy.exceptions import AuthenticationError
from esiosapy.exceptions import ESIOSAPIError
from esiosapy.managers.archive_manager import ArchiveManager
from esiosapy.managers.indicator_manager import IndicatorManager
from esiosapy.managers.offer_indicator_manager import OfferIndicatorManager


__all__ = [
    "APIResponseError",
    "ArchiveManager",
    "AuthenticationError",
    "ESIOSAPIError",
    "ESIOSAPYClient",
    "IndicatorManager",
    "OfferIndicatorManager",
    "__author__",
    "__version__",
]
