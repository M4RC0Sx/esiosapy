from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import AsyncMock

import pytest

from esiosapy.managers.async_offer_indicator_manager import AsyncOfferIndicatorManager


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestAsyncOfferIndicatorManager:
    @pytest.fixture
    def async_offer_indicator_manager(
        self, mocker: MockerFixture
    ) -> AsyncOfferIndicatorManager:
        mock_request_helper = AsyncMock()
        return AsyncOfferIndicatorManager(mock_request_helper)

    def test_initialization(
        self, async_offer_indicator_manager: AsyncOfferIndicatorManager
    ) -> None:
        assert async_offer_indicator_manager.request_helper is not None

    async def test_list_all(
        self,
        async_offer_indicator_manager: AsyncOfferIndicatorManager,
        mocker: MockerFixture,
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {
            "indicators": [
                {
                    "id": 1,
                    "name": "Offer 1",
                    "short_name": "O1",
                    "description": "",
                    "units": "EUR",
                    "timezone": "Europe/Madrid",
                    "taxonomy_terms": [],
                },
                {
                    "id": 2,
                    "name": "Offer 2",
                    "short_name": "O2",
                    "description": "",
                    "units": "EUR",
                    "timezone": "Europe/Madrid",
                    "taxonomy_terms": [],
                },
            ]
        }
        async_offer_indicator_manager.request_helper.get_request = AsyncMock(  # type: ignore[method-assign]
            return_value=mock_response
        )

        indicators = await async_offer_indicator_manager.list_all()

        assert len(indicators) == 2
        async_offer_indicator_manager.request_helper.get_request.assert_called_once_with(
            "/offer_indicators", params={}
        )

    async def test_list_all_with_taxonomy_terms(
        self,
        async_offer_indicator_manager: AsyncOfferIndicatorManager,
        mocker: MockerFixture,
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {"indicators": []}
        async_offer_indicator_manager.request_helper.get_request = AsyncMock(  # type: ignore[method-assign]
            return_value=mock_response
        )

        await async_offer_indicator_manager.list_all(taxonomy_terms=["market", "price"])

        async_offer_indicator_manager.request_helper.get_request.assert_called_once_with(
            "/offer_indicators", params={"taxonomy_terms[]": ["market", "price"]}
        )
