from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import pytest

from esiosapy.managers.archive_manager import ArchiveManager


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestArchiveManager:
    @pytest.fixture
    def archive_manager(self, mocker: MockerFixture) -> ArchiveManager:
        mock_request_helper = mocker.MagicMock()
        return ArchiveManager(mock_request_helper)

    def test_initialization(self, archive_manager: ArchiveManager) -> None:
        assert archive_manager.request_helper is not None

    def test_list_all(
        self, archive_manager: ArchiveManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {"archives": []}
        archive_manager.request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        archive_manager.list_all()

        archive_manager.request_helper.get_request.assert_called_once_with("/archives")  # type: ignore[attr-defined]

    def test_list_by_date(
        self, archive_manager: ArchiveManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {"archives": []}
        archive_manager.request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        archive_manager.list_by_date("2024-01-15")

        archive_manager.request_helper.get_request.assert_called_once_with(  # type: ignore[attr-defined]
            "/archives", params={"date": "2024-01-15"}
        )

    def test_list_by_date_with_datetime(
        self, archive_manager: ArchiveManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {"archives": []}
        archive_manager.request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        archive_manager.list_by_date(datetime(2024, 1, 15, 10, 0, 0))

        archive_manager.request_helper.get_request.assert_called_once()  # type: ignore[attr-defined]

    def test_list_by_date_range(
        self, archive_manager: ArchiveManager, mocker: MockerFixture
    ) -> None:
        mock_response = mocker.MagicMock()
        mock_response.json.return_value = {"archives": []}
        archive_manager.request_helper.get_request.return_value = mock_response  # type: ignore[attr-defined]

        archive_manager.list_by_date_range("2024-01-01", "2024-01-31")

        archive_manager.request_helper.get_request.assert_called_once_with(  # type: ignore[attr-defined]
            "/archives",
            params={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
            },
        )
