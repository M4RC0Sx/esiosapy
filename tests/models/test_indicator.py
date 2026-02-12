from __future__ import annotations

from datetime import datetime
from typing import Any
from unittest.mock import MagicMock

import pytest

from esiosapy.models.indicator.geo_agg import GeoAgg
from esiosapy.models.indicator.geo_trunc import GeoTrunc
from esiosapy.models.indicator.indicator import Indicator
from esiosapy.models.indicator.time_agg import TimeAgg
from esiosapy.models.indicator.time_trunc import TimeTrunc


class TestEnumImports:
    def test_geo_trunc_import(self) -> None:
        from esiosapy.models.indicator.geo_trunc import GeoTrunc

        assert GeoTrunc is not None

    def test_geo_agg_import(self) -> None:
        from esiosapy.models.indicator.geo_agg import GeoAgg

        assert GeoAgg is not None

    def test_time_trunc_import(self) -> None:
        from esiosapy.models.indicator.time_trunc import TimeTrunc

        assert TimeTrunc is not None

    def test_time_agg_import(self) -> None:
        from esiosapy.models.indicator.time_agg import TimeAgg

        assert TimeAgg is not None


class TestIndicatorModel:
    @pytest.fixture
    def mock_request_helper(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def indicator_data(self, mock_request_helper: MagicMock) -> dict[str, Any]:
        return {
            "id": 1,
            "name": "Test Indicator",
            "short_name": "TI",
            "description": "<p>Test description</p>",
            "units": "MWh",
            "timezone": "Europe/Madrid",
            "taxonomy_terms": [],
            "raw": {"id": 1, "name": "Test Indicator"},
            "_request_helper": mock_request_helper,
        }

    def test_initialization(self, indicator_data: dict[str, Any]) -> None:
        indicator = Indicator(**indicator_data)
        assert indicator.id == 1
        assert indicator.name == "Test Indicator"
        assert indicator.short_name == "TI"

    def test_get_data_with_datetime_objects(
        self, indicator_data: dict[str, Any]
    ) -> None:
        indicator = Indicator(**indicator_data)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "indicator": {"values": [{"datetime": "2024-01-01", "value": 100}]}
        }
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        dt_start = datetime(2024, 1, 1, 0, 0, 0)
        dt_end = datetime(2024, 1, 31, 23, 59, 59)

        indicator.get_data(dt_start, dt_end)

        call_args = indicator._request_helper.get_request.call_args  # type: ignore[attr-defined]
        params = call_args[1]["params"]
        assert "start_date" in params
        assert "end_date" in params
        assert params["start_date"] == "2024-01-01T00:00:00.000000"
        assert params["end_date"] == "2024-01-31T23:59:59.000000"

    def test_get_data_with_string_dates(self, indicator_data: dict[str, Any]) -> None:
        indicator = Indicator(**indicator_data)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "indicator": {"values": [{"datetime": "2024-01-01", "value": 100}]}
        }
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        indicator.get_data("2024-01-01", "2024-01-31")

        call_args = indicator._request_helper.get_request.call_args  # type: ignore[attr-defined]
        params = call_args[1]["params"]
        assert params["start_date"] == "2024-01-01"
        assert params["end_date"] == "2024-01-31"

    def test_get_data_with_geo_params(self, indicator_data: dict[str, Any]) -> None:
        indicator = Indicator(**indicator_data)

        mock_response = MagicMock()
        mock_response.json.return_value = {"indicator": {"values": []}}
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        indicator.get_data(
            "2024-01-01",
            "2024-01-31",
            geo_ids=["8741", "8742"],
            geo_agg=GeoAgg.SUM,
            geo_trunc=GeoTrunc.ELECTRIC_SYSTEM,
        )

        call_args = indicator._request_helper.get_request.call_args  # type: ignore[attr-defined]
        params = call_args[1]["params"]
        assert params["geo_ids"] == "8741,8742"
        assert params["geo_agg"] == "sum"
        assert params["geo_trunc"] == "electric_system"

    def test_get_data_with_time_params(self, indicator_data: dict[str, Any]) -> None:
        indicator = Indicator(**indicator_data)

        mock_response = MagicMock()
        mock_response.json.return_value = {"indicator": {"values": []}}
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        indicator.get_data(
            "2024-01-01",
            "2024-01-31",
            time_agg=TimeAgg.AVERAGE,
            time_trunc=TimeTrunc.HOUR,
        )

        call_args = indicator._request_helper.get_request.call_args  # type: ignore[attr-defined]
        params = call_args[1]["params"]
        assert params["time_agg"] == "average"
        assert params["time_trunc"] == "hour"

    def test_get_data_all_raw_data(self, indicator_data: dict[str, Any]) -> None:
        indicator = Indicator(**indicator_data)

        raw_response = {"indicator": {"values": [], "metadata": {"source": "ESIOS"}}}
        mock_response = MagicMock()
        mock_response.json.return_value = raw_response
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        result = indicator.get_data("2024-01-01", "2024-01-31", all_raw_data=True)

        assert result == raw_response

    def test_get_data_returns_values_only_by_default(
        self, indicator_data: dict[str, Any]
    ) -> None:
        indicator = Indicator(**indicator_data)

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "indicator": {"values": [{"datetime": "2024-01-01", "value": 100}]}
        }
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        result = indicator.get_data("2024-01-01", "2024-01-31")

        assert result == [{"datetime": "2024-01-01", "value": 100}]

    def test_get_data_cleans_none_params(self, indicator_data: dict[str, Any]) -> None:
        indicator = Indicator(**indicator_data)

        mock_response = MagicMock()
        mock_response.json.return_value = {"indicator": {"values": []}}
        indicator._request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        indicator.get_data("2024-01-01", "2024-01-31", geo_ids=None, geo_agg=None)

        call_args = indicator._request_helper.get_request.call_args  # type: ignore[attr-defined]
        params = call_args[1]["params"]
        assert "geo_ids" not in params
        assert "geo_agg" not in params
