from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from esiosapy.managers.async_offer_indicator_manager import AsyncOfferIndicatorManager


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestAsyncOfferIndicatorManager:
    @pytest.fixture
    def async_offer_manager(self, mocker: MockerFixture) -> AsyncOfferIndicatorManager:
        mock_request_helper = mocker.MagicMock()
        return AsyncOfferIndicatorManager(mock_request_helper)

    def test_initialization(
        self, async_offer_manager: AsyncOfferIndicatorManager
    ) -> None:
        assert async_offer_manager.request_helper is not None
