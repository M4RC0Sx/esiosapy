from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from esiosapy.managers.async_indicator_manager import AsyncIndicatorManager


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestAsyncIndicatorManager:
    @pytest.fixture
    def async_indicator_manager(self, mocker: MockerFixture) -> AsyncIndicatorManager:
        mock_request_helper = mocker.MagicMock()
        return AsyncIndicatorManager(mock_request_helper)

    def test_initialization(
        self, async_indicator_manager: AsyncIndicatorManager
    ) -> None:
        assert async_indicator_manager.request_helper is not None
