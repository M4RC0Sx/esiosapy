from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from esiosapy.models.indicator.geo_agg import GeoAgg
from esiosapy.models.indicator.geo_trunc import GeoTrunc
from esiosapy.models.indicator.time_agg import TimeAgg
from esiosapy.models.indicator.time_trunc import TimeTrunc
from esiosapy.utils.request_helper import RequestHelper


class Indicator(BaseModel):
    """
    Represents an indicator with associated metadata and methods to retrieve
    and process its data.

    This class models an indicator object, which includes various attributes
    such as its ID, name,
    description, and raw data. It also provides methods to prettify
    the description and to fetch
    the indicator's data over specified date ranges with optional
    geographical and time-based
    aggregations and truncations.
    """

    id: int
    """The unique identifier for the indicator.

    :type: int
    """

    name: str
    """The name of the indicator.

    :type: str
    """

    short_name: str
    """The short name of the indicator.

    :type: str
    """

    description: str
    """A detailed description of the indicator.

    :type: str
    """

    raw: Dict[str, Any]
    """The raw dictionary containing the original data of the indicator.

    :type: Dict[str, Any]
    """

    _request_helper: RequestHelper
    """An instance of RequestHelper used to make API requests.

    :type: RequestHelper
    """

    def __init__(self, **data: Any):
        """
        Initializes the Indicator class with the provided data.

        :param data: The data used to initialize the indicator, including the
                     request helper and other attributes.
        :type data: Any
        """
        super().__init__(**data)
        self._request_helper = data["_request_helper"]

    def prettify_description(self) -> str:
        """
        Converts the HTML description of the indicator into a plain text format
        with better readability.

        :raises ImportError: If `beautifulsoup4` is not installed.
        :return: The prettified description as a plain text string.
        :rtype: str
        """
        try:
            from bs4 import BeautifulSoup  # type: ignore
        except ImportError:
            raise ImportError(
                "The `beautifulsoup4` package is required to prettify the description. "
                "Install it with 'pip install beautifulsoup4' "
                "or with your preferred package manager."
            ) from None

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
        """
        Retrieves the data for the indicator based on the specified parameters.

        :param target_dt_start: The start date and time for data retrieval.
        :type target_dt_start: Union[datetime, str]
        :param target_dt_end: The end date and time for data retrieval.
        :type target_dt_end: Union[datetime, str]
        :param geo_ids: A list of geographical identifiers
                        to filter data, defaults to None.
        :type geo_ids: Optional[List[str]], optional
        :param geo_agg: The geographical aggregation method, defaults to None.
        :type geo_agg: Optional[GeoAgg], optional
        :param geo_trunc: The geographical truncation level, defaults to None.
        :type geo_trunc: Optional[GeoTrunc], optional
        :param time_agg: The time aggregation method, defaults to None.
        :type time_agg: Optional[TimeAgg], optional
        :param time_trunc: The time truncation level, defaults to None.
        :type time_trunc: Optional[TimeTrunc], optional
        :param all_raw_data: Whether to return all raw data or just
                             the indicator values, defaults to False.
        :type all_raw_data: bool, optional
        :return: The retrieved indicator data, either as raw JSON or processed values.
        :rtype: Any
        """
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
