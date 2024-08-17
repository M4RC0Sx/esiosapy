from typing import Dict, List, Optional, Union
from datetime import datetime

from esiosapy.models.archive.archive import Archive
from esiosapy.models.archive.archive_date_type import ArchiveDateType
from esiosapy.utils.request_helper import RequestHelper


class ArchiveManager:
    def __init__(self, request_helper: RequestHelper) -> None:
        self.request_helper = request_helper

    def _init_archive(self, archive: Dict[str, Union[str, int]]) -> Archive:
        return Archive(**archive, raw=archive, _request_helper=self.request_helper)

    def list_all(self) -> List[Archive]:
        response = self.request_helper.get_request("/archives")
        return [self._init_archive(archive) for archive in response.json()["archives"]]

    def list_by_date(
        self,
        target_dt: Union[datetime, str],
        date_type: Optional[ArchiveDateType] = None,
        taxonomy_terms: Optional[List[str]] = None,
    ) -> List[Archive]:
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
