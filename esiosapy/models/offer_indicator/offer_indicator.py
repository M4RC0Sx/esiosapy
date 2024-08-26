from datetime import datetime
from typing import Any, Dict, List, Union

from pydantic import BaseModel

from esiosapy.utils.request_helper import RequestHelper


class OfferIndicator(BaseModel):
    id: int
    """The unique identifier of the offer indicator.

    :type: int
    """

    name: str
    """The name of the offer indicator.

    :type: str
    """

    description: str
    """A detailed description of the offer indicator, often in HTML format.

    :type: str
    """

    raw: Dict[str, Any]
    """Raw data associated with the offer indicator.

    :type: Dict[str, Any]
    """

    _request_helper: RequestHelper
    """A helper object for making HTTP requests.

    :type: RequestHelper
    """

    def __init__(self, **data: Any):
        """
        Initialize the OfferIndicator instance.

        :param data: Arbitrary keyword arguments that initialize the object.
        :type data: Any
        """
        super().__init__(**data)
        self._request_helper = data["_request_helper"]

    def prettify_description(self) -> str:
        """
        Convert the HTML description into a prettified plain-text format.

        This method uses BeautifulSoup to parse and clean the HTML content
        found in the description, returning it as a plain-text string.

        :return: A prettified plain-text version of the description.
        :rtype: str

        :raises ImportError: If the BeautifulSoup package is not installed.
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

    def get_data_by_date(
        self,
        target_dt: Union[datetime, str],
        all_raw_data: bool = False,
    ) -> Any:
        """
        Retrieve the indicator data for a specific date.

        This method fetches the indicator data for a given date, either returning
        the raw JSON response or the specific indicator values.

        :param target_dt: The target date for which to retrieve data,
                          either as a datetime object or a string.
        :type target_dt: Union[datetime, str]
        :param all_raw_data: If True, returns the entire raw JSON response; otherwise,
                             only returns the indicator values.
        :type all_raw_data: bool, optional
        :return: The requested data, either as a raw JSON or
                 as specific indicator values.
        :rtype: Any
        """
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
        """
        Retrieve the indicator data for a specific date range.

        This method fetches the indicator data for a given date range, either returning
        the raw JSON response or the specific indicator values.

        :param target_dt_start: The start date for the range,
                                either as a datetime object or a string.
        :type target_dt_start: Union[datetime, str]
        :param target_dt_end: The end date for the range,
                              either as a datetime object or a string.
        :type target_dt_end: Union[datetime, str]
        :param all_raw_data: If True, returns the entire raw JSON response; otherwise,
                             only returns the indicator values.
        :type all_raw_data: bool, optional
        :return: The requested data, either as a raw JSON or
                 as specific indicator values.
        :rtype: Any
        """
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
