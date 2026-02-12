from __future__ import annotations

from datetime import datetime
from typing import Any
from unittest.mock import MagicMock

import pytest

from esiosapy.models.offer_indicator.offer_indicator import OfferIndicator


class TestOfferIndicatorModel:
    @pytest.fixture
    def mock_request_helper(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def offer_indicator_data(self, mock_request_helper: MagicMock) -> dict[str, Any]:
        return {
            "id": 1,
            "name": "Test Offer Indicator",
            "description": "<p>Test description</p>",
            "raw": {"id": 1, "name": "Test Offer Indicator"},
            "_request_helper": mock_request_helper,
        }

    def test_initialization(self, offer_indicator_data: dict[str, Any]) -> None:
        indicator = OfferIndicator(**offer_indicator_data)
        assert indicator.id == 1
        assert indicator.name == "Test Offer Indicator"

    def test_get_data_by_date_with_datetime(
        self, offer_indicator_data: dict[str, Any]
    ) -> None:
        indicator = OfferIndicator(**offer_indicator_data)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "indicator": {"values": [{"datetime": "2024-01-01", "value": 100}]}
        }
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        dt = datetime(2024, 1, 15, 10, 30, 0)
        indicator.get_data_by_date(dt)

        call_args = indicator._request_helper.get_request.call_args  # type: ignore[attr-defined]
        params = call_args[1]["params"]
        assert params["datetime"] == "2024-01-15T10:30:00.000000"

    def test_get_data_by_date_with_string(
        self, offer_indicator_data: dict[str, Any]
    ) -> None:
        indicator = OfferIndicator(**offer_indicator_data)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "indicator": {"values": [{"datetime": "2024-01-01", "value": 100}]}
        }
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        indicator.get_data_by_date("2024-01-15")

        call_args = indicator._request_helper.get_request.call_args  # type: ignore[attr-defined]
        params = call_args[1]["params"]
        assert params["datetime"] == "2024-01-15"

    def test_get_data_by_date_returns_values_only(
        self, offer_indicator_data: dict[str, Any]
    ) -> None:
        indicator = OfferIndicator(**offer_indicator_data)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "indicator": {"values": [{"datetime": "2024-01-01", "value": 100}]}
        }
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        result = indicator.get_data_by_date("2024-01-15")

        assert result == [{"datetime": "2024-01-01", "value": 100}]

    def test_get_data_by_date_returns_raw_data(
        self, offer_indicator_data: dict[str, Any]
    ) -> None:
        indicator = OfferIndicator(**offer_indicator_data)

        raw_response = {"indicator": {"values": [], "metadata": {"source": "ESIOS"}}}
        mock_response = MagicMock()
        mock_response.json.return_value = raw_response
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        result = indicator.get_data_by_date("2024-01-15", all_raw_data=True)

        assert result == raw_response

    def test_get_data_by_date_range_with_datetime(
        self, offer_indicator_data: dict[str, Any]
    ) -> None:
        indicator = OfferIndicator(**offer_indicator_data)

        mock_response = MagicMock()
        mock_response.json.return_value = {"indicator": {"values": []}}
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        dt_start = datetime(2024, 1, 1, 0, 0, 0)
        dt_end = datetime(2024, 1, 31, 23, 59, 59)
        indicator.get_data_by_date_range(dt_start, dt_end)

        call_args = indicator._request_helper.get_request.call_args  # type: ignore[attr-defined]
        params = call_args[1]["params"]
        assert params["start_date"] == "2024-01-01T00:00:00.000000"
        assert params["end_date"] == "2024-01-31T23:59:59.000000"

    def test_get_data_by_date_range_with_strings(
        self, offer_indicator_data: dict[str, Any]
    ) -> None:
        indicator = OfferIndicator(**offer_indicator_data)

        mock_response = MagicMock()
        mock_response.json.return_value = {"indicator": {"values": []}}
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        indicator.get_data_by_date_range("2024-01-01", "2024-01-31")

        call_args = indicator._request_helper.get_request.call_args  # type: ignore[attr-defined]
        params = call_args[1]["params"]
        assert params["start_date"] == "2024-01-01"
        assert params["end_date"] == "2024-01-31"

    def test_get_data_by_date_range_returns_values_only(
        self, offer_indicator_data: dict[str, Any]
    ) -> None:
        indicator = OfferIndicator(**offer_indicator_data)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "indicator": {"values": [{"datetime": "2024-01-15", "value": 200}]}
        }
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        result = indicator.get_data_by_date_range("2024-01-01", "2024-01-31")

        assert result == [{"datetime": "2024-01-15", "value": 200}]

    def test_get_data_by_date_range_returns_raw_data(
        self, offer_indicator_data: dict[str, Any]
    ) -> None:
        indicator = OfferIndicator(**offer_indicator_data)

        raw_response = {"indicator": {"values": [], "metadata": {"source": "ESIOS"}}}
        mock_response = MagicMock()
        mock_response.json.return_value = raw_response
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        result = indicator.get_data_by_date_range(
            "2024-01-01", "2024-01-31", all_raw_data=True
        )

        assert result == raw_response


class TestOfferIndicatorModelExists:
    def test_offer_indicator_import(self) -> None:
        from esiosapy.models.offer_indicator.offer_indicator import OfferIndicator

        assert callable(OfferIndicator)
