from datetime import datetime
from typing import List, Dict, Any, Union

from pydantic import BaseModel

from esiosapy.utils.request_helper import RequestHelper


class OfferIndicator(BaseModel):
    id: int
    name: str
    description: str
    raw: Dict[str, Any]

    _request_helper: RequestHelper

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._request_helper = data["_request_helper"]

    def prettify_description(self) -> str:
        try:
            from bs4 import BeautifulSoup  # type: ignore
        except ImportError:
            raise ImportError(
                "The `beautifulsoup4` package is required to prettify the description. Install it with 'pip install beautifulsoup4' or with your preferred package manager."
            )

        soup = BeautifulSoup(self.description, "html.parser")
        text = soup.get_text(separator="\n").strip()

        return str(text)

    def get_data_by_date(
        self,
        target_dt: Union[datetime, str],
        all_raw_data: bool = False,
    ) -> Any:
        if isinstance(target_dt, datetime):
            target_dt = target_dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        params: Dict[str, Union[str, int, List[str]]] = {
            "datetime": target_dt,
        }

        response = self._request_helper.get_request(
            f"/offer_indicators/{self.id}", params=params
        )

        return (
            response.json() if all_raw_data else response.json()["indicator"]["values"]
        )

    def get_data_by_date_range(
        self,
        target_dt_start: Union[datetime, str],
        target_dt_end: Union[datetime, str],
        all_raw_data: bool = False,
    ) -> Any:
        if isinstance(target_dt_start, datetime):
            target_dt_start = target_dt_start.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        if isinstance(target_dt_end, datetime):
            target_dt_end = target_dt_end.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        params: Dict[str, Union[str, int, List[str]]] = {
            "start_date": target_dt_start,
            "end_date": target_dt_end,
        }

        response = self._request_helper.get_request(
            f"/offer_indicators/{self.id}", params=params
        )

        return (
            response.json() if all_raw_data else response.json()["indicator"]["values"]
        )
