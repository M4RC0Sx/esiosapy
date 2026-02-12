from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

import pytest

from esiosapy.managers.indicator_manager import IndicatorManager


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestIndicatorManager:
    @pytest.fixture
    def indicator_manager(self, mocker: MockerFixture) -> IndicatorManager:
        mock_request_helper = mocker.MagicMock()
        return IndicatorManager(mock_request_helper)

    @pytest.fixture
    def mock_indicator_data(self) -> dict[str, Any]:
        return {
            "id": 1,
            "name": "Test Indicator",
            "short_name": "TI",
            "description": "<p>Test description</p>",
            "units": "MWh",
            "timezone": "Europe/Madrid",
            "taxonomy_terms": [{"id": 1, "name": "energy"}],
        }

    def test_initialization(self, indicator_manager: IndicatorManager) -> None:
        assert indicator_manager.request_helper is not None

    def test_init_indicator(
        self, indicator_manager: IndicatorManager, mock_indicator_data: dict[str, Any]
    ) -> None:
        indicator = indicator_manager._init_indicator(mock_indicator_data)
        assert indicator.id == 1
        assert indicator.name == "Test Indicator"
        assert indicator.short_name == "TI"
        assert indicator.raw == mock_indicator_data

    def test_list_all(
        self, indicator_manager: IndicatorManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {
            "indicators": [
                {
                    "id": 1,
                    "name": "Indicator 1",
                    "short_name": "I1",
                    "description": "",
                    "units": "MWh",
                    "timezone": "Europe/Madrid",
                    "taxonomy_terms": [],
                },
                {
                    "id": 2,
                    "name": "Indicator 2",
                    "short_name": "I2",
                    "description": "",
                    "units": "MW",
                    "timezone": "Europe/Madrid",
                    "taxonomy_terms": [],
                },
            ]
        }
        indicator_manager.request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        indicators = indicator_manager.list_all()

        assert len(indicators) == 2
        indicator_manager.request_helper.get_request.assert_called_once_with(  # type: ignore[attr-defined]
            "/indicators", params={}
        )

    def test_list_all_with_taxonomy_terms(
        self, indicator_manager: IndicatorManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {"indicators": []}
        indicator_manager.request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        indicator_manager.list_all(taxonomy_terms=["energy", "power"])

        indicator_manager.request_helper.get_request.assert_called_once_with(  # type: ignore[attr-defined]
            "/indicators", params={"taxonomy_terms[]": ["energy", "power"]}
        )

    def test_search(
        self, indicator_manager: IndicatorManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {
            "indicators": [
                {
                    "id": 1,
                    "name": "Wind Energy",
                    "short_name": "WE",
                    "description": "",
                    "units": "MWh",
                    "timezone": "Europe/Madrid",
                    "taxonomy_terms": [],
                }
            ]
        }
        indicator_manager.request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        indicators = indicator_manager.search("wind")

        assert len(indicators) == 1
        indicator_manager.request_helper.get_request.assert_called_once_with(  # type: ignore[attr-defined]
            "/indicators", params={"text": "wind"}
        )
