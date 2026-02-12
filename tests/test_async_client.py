from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from esiosapy.async_client import AsyncESIOSAPYClient


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestAsyncESIOSAPYClient:
    @pytest.fixture
    def async_esios_client(self, mocker: MockerFixture) -> AsyncESIOSAPYClient:
        mocker.patch("esiosapy.async_client._HTTPX_AVAILABLE", True)
        mocker.patch("esiosapy.managers.async_archive_manager.AsyncArchiveManager")
        mocker.patch("esiosapy.managers.async_indicator_manager.AsyncIndicatorManager")
        mocker.patch(
            "esiosapy.managers.async_offer_indicator_manager.AsyncOfferIndicatorManager"
        )

        return AsyncESIOSAPYClient(
            token="test-token", base_url="https://api.example.com"
        )

    def test_initialization(
        self, async_esios_client: AsyncESIOSAPYClient, mocker: MockerFixture
    ) -> None:
        assert async_esios_client.token == "test-token"
        assert async_esios_client.base_url == "https://api.example.com"


class TestAsyncESIOSAPYClientImportError:
    def test_import_error_when_httpx_not_available(self, mocker: MockerFixture) -> None:
        mocker.patch("esiosapy.async_client._HTTPX_AVAILABLE", False)

        with pytest.raises(ImportError, match="httpx"):
            AsyncESIOSAPYClient(token="test")
