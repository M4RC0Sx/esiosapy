from datetime import datetime
from typing import Dict, List, Optional, Union

from esiosapy.models.archive.archive import Archive
from esiosapy.models.archive.archive_date_type import ArchiveDateType
from esiosapy.utils.request_helper import RequestHelper


class ArchiveManager:
    """
    Manages archive-related operations for the ESIOS API.

    This class provides methods to retrieve and filter archives from the ESIOS
    API, such as listing all archives or filtering them by date or date range.
    """

    def __init__(self, request_helper: RequestHelper) -> None:
        """
        Initializes the ArchiveManager with a RequestHelper.

        :param request_helper: An instance of RequestHelper used to make API requests.
        :type request_helper: RequestHelper
        """
        self.request_helper = request_helper

    def _init_archive(self, archive: Dict[str, Union[str, int]]) -> Archive:
        """
        Initializes an Archive object from a dictionary of archive data.

        :param archive: A dictionary containing archive data.
        :type archive: Dict[str, Union[str, int]]
        :return: An Archive object initialized with the provided data.
        :rtype: Archive
        """
        return Archive(**archive, raw=archive, _request_helper=self.request_helper)

    def list_all(self) -> List[Archive]:
        """
        Retrieves a list of all archives.

        This method sends a GET request to the `/archives` endpoint and
        returns a list of Archive objects representing all available archives.

        :return: A list of Archive objects representing all archives.
        :rtype: List[Archive]
        """
        response = self.request_helper.get_request("/archives")
        return [self._init_archive(archive) for archive in response.json()["archives"]]

    def list_by_date(
        self,
        target_dt: Union[datetime, str],
        date_type: Optional[ArchiveDateType] = None,
        taxonomy_terms: Optional[List[str]] = None,
    ) -> List[Archive]:
        """
        Retrieves a list of archives filtered by a specific date.

        This method sends a GET request to the `/archives` endpoint with filters
        based on the provided date, date type, and optional taxonomy terms.

        :param target_dt: The target date for filtering archives. Can be a datetime
                          object or an ISO 8601 formatted string.
        :type target_dt: Union[datetime, str]
        :param date_type: The type of date to filter by (e.g., publication date),
                          defaults to None.
        :type date_type: Optional[ArchiveDateType], optional
        :param taxonomy_terms: A list of taxonomy terms to further filter the archives,
                               defaults to None.
        :type taxonomy_terms: Optional[List[str]], optional
        :return: A list of Archive objects filtered by the specified date.
        :rtype: List[Archive]
        """
        if isinstance(target_dt, datetime):
            target_dt = target_dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        params: Dict[str, Union[str, int, List[str]]] = {"date": target_dt}
        if date_type:
            params["date_type"] = date_type.value
        if taxonomy_terms:
            params["taxonomy_terms[]"] = taxonomy_terms

        response = self.request_helper.get_request("/archives", params=params)
        return [self._init_archive(archive) for archive in response.json()["archives"]]

    def list_by_date_range(
        self,
        target_dt_start: Union[datetime, str],
        target_dt_end: Union[datetime, str],
        date_type: Optional[ArchiveDateType] = None,
        taxonomy_terms: Optional[List[str]] = None,
    ) -> List[Archive]:
        """
        Retrieves a list of archives filtered by a date range.

        This method sends a GET request to the `/archives` endpoint with filters
        based on the provided start and end dates, date type, and optional taxonomy
        terms.

        :param target_dt_start: The start date for filtering archives. Can be a datetime
                                object or an ISO 8601 formatted string.
        :type target_dt_start: Union[datetime, str]
        :param target_dt_end: The end date for filtering archives. Can be a datetime
                              object or an ISO 8601 formatted string.
        :type target_dt_end: Union[datetime, str]
        :param date_type: The type of date to filter by (e.g., publication date),
                          defaults to None.
        :type date_type: Optional[ArchiveDateType], optional
        :param taxonomy_terms: A list of taxonomy terms to further filter the archives,
                               defaults to None.
        :type taxonomy_terms: Optional[List[str]], optional
        :return: A list of Archive objects filtered by the specified date range.
        :rtype: List[Archive]
        """
        if isinstance(target_dt_start, datetime):
            target_dt_start = target_dt_start.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        if isinstance(target_dt_end, datetime):
            target_dt_end = target_dt_end.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        params: Dict[str, Union[str, int, List[str]]] = {
            "start_date": target_dt_start,
            "end_date": target_dt_end,
        }
        if date_type:
            params["date_type"] = date_type.value
        if taxonomy_terms:
            params["taxonomy_terms[]"] = taxonomy_terms

        response = self.request_helper.get_request("/archives", params=params)
        return [self._init_archive(archive) for archive in response.json()["archives"]]
