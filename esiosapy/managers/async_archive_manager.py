from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Union

from esiosapy.models.archive.archive import Archive


if TYPE_CHECKING:
    from esiosapy.utils.async_request_helper import AsyncRequestHelper


class AsyncArchiveManager:
    """
    Manages archive-related operations for the ESIOS API (async version).

    This class provides methods to retrieve archives from the ESIOS API,
    including listing all archives and filtering by date.
    """

    def __init__(self, request_helper: AsyncRequestHelper) -> None:
        """
        Initializes the AsyncArchiveManager with an AsyncRequestHelper.

        :param request_helper: An instance of AsyncRequestHelper used to make API requests.
        :type request_helper: AsyncRequestHelper
        """
        self.request_helper = request_helper

    def _init_archive(self, archive: dict[str, Union[str, int]]) -> Archive:
        """
        Initializes an Archive object from a dictionary of archive data.

        :param archive: A dictionary containing archive data.
        :type archive: Dict[str, Union[str, int]]
        :return: An Archive object initialized with the provided data.
        :rtype: Archive
        """
        return Archive(**archive, raw=archive, _request_helper=self.request_helper)

    async def list_all(
        self,
        page: int = 1,
        per_page: int = 50,
        only_files: bool = False,
    ) -> list[Archive]:
        """
        Retrieves a list of all archives, optionally filtered by page and per_page.

        This method sends a GET request to the `/archives` endpoint and
        returns a list of Archive objects.

        :param page: The page number for pagination, defaults to 1.
        :type page: int, optional
        :param per_page: The number of archives per page, defaults to 50.
        :type per_page: int, optional
        :param only_files: If True, only returns archives with files, defaults to False.
        :type only_files: bool, optional
        :return: A list of Archive objects representing all (or filtered) archives.
        :rtype: list[Archive]
        """
        params: dict[str, Union[str, int, bool]] = {
            "page": page,
            "per_page": per_page,
            "only_files": only_files,
        }

        response = await self.request_helper.get_request("/archives", params=params)
        return [self._init_archive(archive) for archive in response.json()["archives"]]

    async def list_by_date(
        self,
        date_time: str,
        page: int = 1,
        per_page: int = 50,
        only_files: bool = False,
    ) -> list[Archive]:
        """
        Retrieves archives for a specific date.

        This method sends a GET request to the `/archives` endpoint filtered
        by a specific date and returns a list of Archive objects.

        :param date_time: The date for which to retrieve archives (ISO format).
        :type date_time: str
        :param page: The page number for pagination, defaults to 1.
        :type page: int, optional
        :param per_page: The number of archives per page, defaults to 50.
        :type per_page: int, optional
        :param only_files: If True, only returns archives with files, defaults to False.
        :type only_files: bool, optional
        :return: A list of Archive objects for the specified date.
        :rtype: list[Archive]
        """
        params: dict[str, Union[str, int, bool]] = {
            "date": date_time,
            "page": page,
            "per_page": per_page,
            "only_files": only_files,
        }

        response = await self.request_helper.get_request("/archives", params=params)
        return [self._init_archive(archive) for archive in response.json()["archives"]]

    async def list_by_date_range(
        self,
        start_date: str,
        end_date: str,
        page: int = 1,
        per_page: int = 50,
        only_files: bool = False,
    ) -> list[Archive]:
        """
        Retrieves archives within a date range.

        This method sends a GET request to the `/archives` endpoint filtered
        by a start and end date and returns a list of Archive objects.

        :param start_date: The start date of the range (ISO format).
        :type start_date: str
        :param end_date: The end date of the range (ISO format).
        :type end_date: str
        :param page: The page number for pagination, defaults to 1.
        :type page: int, optional
        :param per_page: The number of archives per page, defaults to 50.
        :type per_page: int, optional
        :param only_files: If True, only returns archives with files, defaults to False.
        :type only_files: bool, optional
        :return: A list of Archive objects within the specified date range.
        :rtype: list[Archive]
        """
        params: dict[str, Union[str, int, bool]] = {
            "start_date": start_date,
            "end_date": end_date,
            "page": page,
            "per_page": per_page,
            "only_files": only_files,
        }

        response = await self.request_helper.get_request("/archives", params=params)
        return [self._init_archive(archive) for archive in response.json()["archives"]]
