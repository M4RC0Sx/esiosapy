from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional
from typing import Union

from esiosapy.managers.base import BaseArchiveManager
from esiosapy.utils.async_request_helper import AsyncRequestHelper


if TYPE_CHECKING:
    from esiosapy.models.archive.archive import Archive
    from esiosapy.models.archive.archive_date_type import ArchiveDateType


class AsyncArchiveManager(BaseArchiveManager[AsyncRequestHelper]):
    """
    Manages archive-related operations for the ESIOS API (async version).

    This class provides methods to retrieve archives from the ESIOS API,
    including listing all archives and filtering by date.
    """

    def __init__(self, request_helper: AsyncRequestHelper) -> None:
        """
        Initializes the AsyncArchiveManager with an AsyncRequestHelper.

        :param request_helper: An instance of AsyncRequestHelper used to make API requests.
        """
        super().__init__(request_helper)

    async def list_all(self) -> list[Archive]:
        """
        Retrieves a list of all archives.

        This method sends a GET request to the `/archives` endpoint and
        returns a list of Archive objects representing all available archives.

        :return: A list of Archive objects representing all archives.
        """
        response = await self.request_helper.get_request(self._endpoint)
        return [self._init_archive(archive) for archive in response.json()["archives"]]

    async def list_by_date(
        self,
        target_dt: Union[datetime, str],
        date_type: Optional[ArchiveDateType] = None,
        taxonomy_terms: Optional[list[str]] = None,
    ) -> list[Archive]:
        """
        Retrieves a list of archives filtered by a specific date.

        This method sends a GET request to the `/archives` endpoint with filters
        based on the provided date, date type, and optional taxonomy terms.

        :param target_dt: The target date for filtering archives. Can be a datetime
                          object or an ISO 8601 formatted string.
        :param date_type: The type of date to filter by (e.g., publication date),
                          defaults to None.
        :param taxonomy_terms: A list of taxonomy terms to further filter the archives,
                               defaults to None.
        :return: A list of Archive objects filtered by the specified date.
        """
        if isinstance(target_dt, datetime):
            target_dt = target_dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        params: dict[str, Union[str, int, list[str]]] = {"date": target_dt}
        if date_type:
            params["date_type"] = date_type.value
        if taxonomy_terms:
            params["taxonomy_terms[]"] = taxonomy_terms

        response = await self.request_helper.get_request(self._endpoint, params=params)
        return [self._init_archive(archive) for archive in response.json()["archives"]]

    async def list_by_date_range(
        self,
        target_dt_start: Union[datetime, str],
        target_dt_end: Union[datetime, str],
        date_type: Optional[ArchiveDateType] = None,
        taxonomy_terms: Optional[list[str]] = None,
    ) -> list[Archive]:
        """
        Retrieves a list of archives filtered by a date range.

        This method sends a GET request to the `/archives` endpoint with filters
        based on the provided start and end dates, date type, and optional taxonomy
        terms.

        :param target_dt_start: The start date for filtering archives. Can be a datetime
                                object or an ISO 8601 formatted string.
        :param target_dt_end: The end date for filtering archives. Can be a datetime
                              object or an ISO 8601 formatted string.
        :param date_type: The type of date to filter by (e.g., publication date),
                          defaults to None.
        :param taxonomy_terms: A list of taxonomy terms to further filter the archives,
                               defaults to None.
        :return: A list of Archive objects filtered by the specified date range.
        """
        if isinstance(target_dt_start, datetime):
            target_dt_start = target_dt_start.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        if isinstance(target_dt_end, datetime):
            target_dt_end = target_dt_end.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        params: dict[str, Union[str, int, list[str]]] = {
            "start_date": target_dt_start,
            "end_date": target_dt_end,
        }
        if date_type:
            params["date_type"] = date_type.value
        if taxonomy_terms:
            params["taxonomy_terms[]"] = taxonomy_terms

        response = await self.request_helper.get_request(self._endpoint, params=params)
        return [self._init_archive(archive) for archive in response.json()["archives"]]
