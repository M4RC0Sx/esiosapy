from datetime import datetime
from typing import List, Dict, Any, Optional, Union

from pydantic import BaseModel

from esiosapy.models.indicator.geo_agg import GeoAgg
from esiosapy.models.indicator.geo_trunc import GeoTrunc
from esiosapy.models.indicator.time_agg import TimeAgg
from esiosapy.models.indicator.time_trunc import TimeTrunc
from esiosapy.utils.request_helper import RequestHelper


class Indicator(BaseModel):
    id: int
    name: str
    short_name: str
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

    def get_data(
        self,
        target_dt_start: Union[datetime, str],
        target_dt_end: Union[datetime, str],
        geo_ids: Optional[List[str]] = None,
        geo_agg: Optional[GeoAgg] = None,
        geo_trunc: Optional[GeoTrunc] = None,
        time_agg: Optional[TimeAgg] = None,
        time_trunc: Optional[TimeTrunc] = None,
        all_raw_data: bool = False,
    ) -> Any:
        if isinstance(target_dt_start, datetime):
            target_dt_start = target_dt_start.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        if isinstance(target_dt_end, datetime):
            target_dt_end = target_dt_end.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        params: Dict[str, Optional[Union[str, int, List[str]]]] = {
            "start_date": target_dt_start,
            "end_date": target_dt_end,
            "geo_ids": ",".join(geo_ids) if geo_ids else None,
            "geo_agg": geo_agg.value if geo_agg else None,
            "geo_trunc": geo_trunc.value if geo_trunc else None,
            "time_agg": time_agg.value if time_agg else None,
            "time_trunc": time_trunc.value if time_trunc else None,
        }
        clean_params = {k: v for k, v in params.items() if v is not None}

        response = self._request_helper.get_request(
            f"/indicators/{self.id}", params=clean_params
        )

        return (
            response.json() if all_raw_data else response.json()["indicator"]["values"]
        )
