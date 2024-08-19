from typing import Dict
from urllib.parse import urljoin

import pytest
import requests
from pytest_mock import MockerFixture

from esiosapy.client import ESIOSAPYClient
from esiosapy.managers.archive_manager import ArchiveManager
from esiosapy.managers.indicator_manager import IndicatorManager
from esiosapy.managers.offer_indicator_manager import OfferIndicatorManager
from esiosapy.utils.request_helper import RequestHelper


class TestESIOSAPYClient:
    @pytest.fixture
    def esios_client(self, mocker: MockerFixture) -> ESIOSAPYClient:
        mock_request_helper = mocker.patch(
            "esiosapy.client.RequestHelper", autospec=True
        )
        mock_archive_manager = mocker.patch(  # noqa: F841
            "esiosapy.client.ArchiveManager", autospec=True
        )
        mock_indicator_manager = mocker.patch(  # noqa: F841
            "esiosapy.client.IndicatorManager", autospec=True
        )
        mock_offer_indicator_manager = mocker.patch(  # noqa: F841
            "esiosapy.client.OfferIndicatorManager", autospec=True
        )

        mock_add_default_headers = mock_request_helper.return_value.add_default_headers

        def add_default_headers_side_effect(headers: Dict[str, str]) -> Dict[str, str]:
            default_headers = {
                "Accept": "application/json; application/vnd.esios-api-v1+json",
                "Content-Type": "application/json",
                "x-api-key": "test-token",
            }
            default_headers.update(headers)
            return default_headers

        mock_add_default_headers.side_effect = add_default_headers_side_effect

        return ESIOSAPYClient(token="test-token", base_url="https://api.example.com")

    def test_initialization(
        self, esios_client: ESIOSAPYClient, mocker: MockerFixture
    ) -> None:
        assert esios_client.token == "test-token"
        assert esios_client.base_url == "https://api.example.com"
        assert isinstance(esios_client.request_helper, RequestHelper)
        assert isinstance(esios_client.archives, ArchiveManager)
        assert isinstance(esios_client.indicators, IndicatorManager)
        assert isinstance(esios_client.offer_indicators, OfferIndicatorManager)

    def test_raw_request_with_absolute_url(
        self, esios_client: ESIOSAPYClient, mocker: MockerFixture
    ) -> None:
        mock_get = mocker.patch("requests.get", autospec=True)
        mock_response = mocker.Mock()
        mock_get.return_value = mock_response

        url: str = "https://api.example.com/data"
        headers: Dict[str, str] = {"Custom-Header": "value"}

        response: requests.Response = esios_client.raw_request(url, headers)

        expected_headers: Dict[str, str] = {
            "Accept": "application/json; application/vnd.esios-api-v1+json",
            "Content-Type": "application/json",
            "x-api-key": "test-token",
            "Custom-Header": "value",
        }

        mock_get.assert_called_once_with(url, headers=expected_headers)
        assert response == mock_response

    def test_raw_request_with_relative_url(
        self, esios_client: ESIOSAPYClient, mocker: MockerFixture
    ) -> None:
        mock_get = mocker.patch("requests.get", autospec=True)
        mock_response = mocker.Mock()
        mock_get.return_value = mock_response

        url: str = "/data"
        headers: Dict[str, str] = {}

        expected_url: str = urljoin(esios_client.base_url, url)
        expected_headers: Dict[str, str] = {
            "Accept": "application/json; application/vnd.esios-api-v1+json",
            "Content-Type": "application/json",
            "x-api-key": "test-token",
        }

        response: requests.Response = esios_client.raw_request(url, headers)

        mock_get.assert_called_once_with(expected_url, headers=expected_headers)
        assert response == mock_response
