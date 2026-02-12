from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from esiosapy.managers.async_archive_manager import AsyncArchiveManager


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestAsyncArchiveManager:
    @pytest.fixture
    def async_archive_manager(self, mocker: MockerFixture) -> AsyncArchiveManager:
        mock_request_helper = mocker.MagicMock()
        return AsyncArchiveManager(mock_request_helper)

    def test_initialization(self, async_archive_manager: AsyncArchiveManager) -> None:
        assert async_archive_manager.request_helper is not None
