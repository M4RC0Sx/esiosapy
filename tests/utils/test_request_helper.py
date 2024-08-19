from typing import Dict, List, Union
from urllib.parse import urljoin

import pytest
import requests
from pytest_mock import MockerFixture

from esiosapy.utils.request_helper import RequestHelper


class TestRequestHelper:
    @pytest.fixture
    def request_helper(self) -> RequestHelper:
        return RequestHelper(base_url="https://api.example.com", token="test-token")

    def test_add_default_headers_with_empty_headers(
        self, request_helper: RequestHelper
    ) -> None:
        headers: Dict[str, str] = {}
        expected_headers: Dict[str, str] = {
            "Accept": "application/json; application/vnd.esios-api-v1+json",
            "Content-Type": "application/json",
            "x-api-key": "test-token",
        }

        result = request_helper.add_default_headers(headers)

        assert result == expected_headers

    def test_add_default_headers_with_existing_headers(
        self, request_helper: RequestHelper
    ) -> None:
        headers: Dict[str, str] = {
            "Accept": "text/html",
            "Content-Type": "application/xml",
            "x-api-key": "another-token",
        }

        result = request_helper.add_default_headers(headers)

        assert result == headers

    def test_add_default_headers_with_partial_headers(
        self, request_helper: RequestHelper
    ) -> None:
        headers: Dict[str, str] = {"Accept": "text/plain"}
        expected_headers: Dict[str, str] = {
            "Accept": "text/plain",
            "Content-Type": "application/json",
            "x-api-key": "test-token",
        }

        result = request_helper.add_default_headers(headers)

        assert result == expected_headers

    def test_get_request_success(
        self, mocker: MockerFixture, request_helper: RequestHelper
    ) -> None:
        mock_get = mocker.patch("requests.get")

        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = mocker.Mock()
        mock_response.json.return_value = {"data": "some data"}
        mock_get.return_value = mock_response

        path: str = "/data"
        headers: Dict[str, str] = {}
        params: Dict[str, Union[str, int, List[str]]] = {
            "param1": "value1",
            "param2": 2,
        }

        expected_url: str = urljoin("https://api.example.com", path)
        expected_headers: Dict[str, str] = {
            "Accept": "application/json; application/vnd.esios-api-v1+json",
            "Content-Type": "application/json",
            "x-api-key": "test-token",
        }

        response = request_helper.get_request(path, headers, params)

        mock_get.assert_called_once_with(
            expected_url, headers=expected_headers, params=params
        )

        assert response == mock_response

    def test_get_request_failure(
        self, mocker: MockerFixture, request_helper: RequestHelper
    ) -> None:
        # Mock the requests.get method
        mock_get = mocker.patch("requests.get")

        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("Error")
        mock_get.return_value = mock_response

        path: str = "/data"
        headers: Dict[str, str] = {}
        params: Dict[str, Union[str, int, List[str]]] = {
            "param1": "value1",
            "param2": 2,
        }

        with pytest.raises(requests.HTTPError):
            request_helper.get_request(path, headers, params)

        mock_get.assert_called_once()
