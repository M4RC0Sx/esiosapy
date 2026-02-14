from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from unittest.mock import AsyncMock

import pytest

from esiosapy.managers.async_indicator_manager import AsyncIndicatorManager


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestAsyncIndicatorManager:
    @pytest.fixture
    def async_indicator_manager(self, mocker: MockerFixture) -> AsyncIndicatorManager:
        mock_request_helper = AsyncMock()
        return AsyncIndicatorManager(mock_request_helper)

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

    def test_initialization(
        self, async_indicator_manager: AsyncIndicatorManager
    ) -> None:
        assert async_indicator_manager.request_helper is not None

    async def test_list_all(
        self, async_indicator_manager: AsyncIndicatorManager, mocker: MockerFixture
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
        async_indicator_manager.request_helper.get_request = AsyncMock(  # type: ignore[method-assign]
            return_value=mock_response
        )

        indicators = await async_indicator_manager.list_all()

        assert len(indicators) == 2
        async_indicator_manager.request_helper.get_request.assert_called_once_with(
            "/indicators", params={}
        )

    async def test_list_all_with_taxonomy_terms(
        self, async_indicator_manager: AsyncIndicatorManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {"indicators": []}
        async_indicator_manager.request_helper.get_request = AsyncMock(  # type: ignore[method-assign]
            return_value=mock_response
        )

        await async_indicator_manager.list_all(taxonomy_terms=["energy", "power"])

        async_indicator_manager.request_helper.get_request.assert_called_once_with(
            "/indicators", params={"taxonomy_terms[]": ["energy", "power"]}
        )

    async def test_search(
        self, async_indicator_manager: AsyncIndicatorManager, mocker: MockerFixture
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
        async_indicator_manager.request_helper.get_request = AsyncMock(  # type: ignore[method-assign]
            return_value=mock_response
        )

        indicators = await async_indicator_manager.search("wind")

        assert len(indicators) == 1
        async_indicator_manager.request_helper.get_request.assert_called_once_with(
            "/indicators", params={"text": "wind"}
        )
