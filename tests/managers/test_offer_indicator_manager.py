from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from esiosapy.managers.offer_indicator_manager import OfferIndicatorManager


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestOfferIndicatorManager:
    @pytest.fixture
    def offer_indicator_manager(self, mocker: MockerFixture) -> OfferIndicatorManager:
        mock_request_helper = mocker.MagicMock()
        return OfferIndicatorManager(mock_request_helper)

    def test_initialization(
        self, offer_indicator_manager: OfferIndicatorManager
    ) -> None:
        assert offer_indicator_manager.request_helper is not None

    def test_list_all(
        self, offer_indicator_manager: OfferIndicatorManager, mocker: MockerFixture
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
        offer_indicator_manager.request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        indicators = offer_indicator_manager.list_all()

        assert len(indicators) == 2
        offer_indicator_manager.request_helper.get_request.assert_called_once_with(  # type: ignore[attr-defined]
            "/offer_indicators", params={}
        )

    def test_list_all_with_taxonomy_terms(
        self, offer_indicator_manager: OfferIndicatorManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {"indicators": []}
        offer_indicator_manager.request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        offer_indicator_manager.list_all(taxonomy_terms=["market", "price"])

        offer_indicator_manager.request_helper.get_request.assert_called_once_with(  # type: ignore[attr-defined]
            "/offer_indicators", params={"taxonomy_terms[]": ["market", "price"]}
        )
