from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock

import pytest

from esiosapy.managers.async_archive_manager import AsyncArchiveManager


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestAsyncArchiveManager:
    @pytest.fixture
    def async_archive_manager(self, mocker: MockerFixture) -> AsyncArchiveManager:
        mock_request_helper = AsyncMock()
        return AsyncArchiveManager(mock_request_helper)

    def test_initialization(self, async_archive_manager: AsyncArchiveManager) -> None:
        assert async_archive_manager.request_helper is not None

    async def test_list_all(
        self, async_archive_manager: AsyncArchiveManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {"archives": []}
        async_archive_manager.request_helper.get_request = AsyncMock(  # type: ignore[method-assign]
            return_value=mock_response
        )

        await async_archive_manager.list_all()

        async_archive_manager.request_helper.get_request.assert_called_once_with(
            "/archives"
        )

    async def test_list_by_date(
        self, async_archive_manager: AsyncArchiveManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {"archives": []}
        async_archive_manager.request_helper.get_request = AsyncMock(  # type: ignore[method-assign]
            return_value=mock_response
        )

        await async_archive_manager.list_by_date("2024-01-15")

        async_archive_manager.request_helper.get_request.assert_called_once_with(
            "/archives", params={"date": "2024-01-15"}
        )

    async def test_list_by_date_with_datetime(
        self, async_archive_manager: AsyncArchiveManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {"archives": []}
        async_archive_manager.request_helper.get_request = AsyncMock(  # type: ignore[method-assign]
            return_value=mock_response
        )

        await async_archive_manager.list_by_date(datetime(2024, 1, 15, 10, 0, 0))

        async_archive_manager.request_helper.get_request.assert_called_once()

    async def test_list_by_date_range(
        self, async_archive_manager: AsyncArchiveManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {"archives": []}
        async_archive_manager.request_helper.get_request = AsyncMock(  # type: ignore[method-assign]
            return_value=mock_response
        )

        await async_archive_manager.list_by_date_range("2024-01-01", "2024-01-31")

        async_archive_manager.request_helper.get_request.assert_called_once_with(
            "/archives",
            params={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
            },
        )
