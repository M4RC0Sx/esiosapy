from __future__ import annotations

from unittest.mock import MagicMock

import pytest
import requests

from requests.exceptions import HTTPError
from requests.exceptions import RequestException

from esiosapy.exceptions import APIResponseError
from esiosapy.exceptions import AuthenticationError
from esiosapy.exceptions import ESIOSAPIError
from esiosapy.utils.request_helper import RequestHelper


class TestRequestHelper:
    @pytest.fixture
    def mock_session(self) -> MagicMock:
        """Create a mock session with mocked get method."""
        mock = MagicMock()
        mock.get.return_value = MagicMock()
        return mock

    @pytest.fixture
    def request_helper(self, mock_session: MagicMock) -> RequestHelper:
        """Create a RequestHelper with mocked session."""
        helper = RequestHelper(base_url="https://api.example.com", token="test-token")
        helper._session = mock_session
        return helper

    def test_add_default_headers_with_empty_headers(
        self, request_helper: RequestHelper
    ) -> None:
        headers: dict[str, str] = {}
        expected_headers: dict[str, str] = {
            "Accept": "application/json; application/vnd.esios-api-v1+json",
            "Content-Type": "application/json",
            "x-api-key": "test-token",
        }

        result = request_helper.add_default_headers(headers)

        assert result == expected_headers

    def test_add_default_headers_with_existing_headers(
        self, request_helper: RequestHelper
    ) -> None:
        headers: dict[str, str] = {
            "Accept": "text/html",
            "Content-Type": "application/xml",
            "x-api-key": "another-token",
        }

        result = request_helper.add_default_headers(headers)

        assert result == headers

    def test_add_default_headers_with_partial_headers(
        self, request_helper: RequestHelper
    ) -> None:
        headers: dict[str, str] = {"Accept": "text/plain"}
        expected_headers: dict[str, str] = {
            "Accept": "text/plain",
            "Content-Type": "application/json",
            "x-api-key": "test-token",
        }

        result = request_helper.add_default_headers(headers)

        assert result == expected_headers

    def test_session_is_created(self) -> None:
        helper = RequestHelper(base_url="https://api.example.com", token="test-token")
        assert hasattr(helper, "_session")
        assert isinstance(helper._session, requests.Session)

    def test_get_request_with_none_headers_and_params(
        self, request_helper: RequestHelper, mock_session: MagicMock
    ) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_session.get.return_value = mock_response

        response = request_helper.get_request("/test")

        mock_session.get.assert_called_once()
        call_args = mock_session.get.call_args
        assert call_args[1]["headers"]["x-api-key"] == "test-token"
        assert call_args[1]["params"] == {}
        assert response == mock_response

    def test_get_request_with_custom_headers_and_params(
        self, request_helper: RequestHelper, mock_session: MagicMock
    ) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test"}
        mock_session.get.return_value = mock_response

        response = request_helper.get_request(
            "/test", headers={"Accept": "text/xml"}, params={"page": 1}
        )

        call_args = mock_session.get.call_args
        assert call_args[1]["headers"]["Accept"] == "text/xml"
        assert call_args[1]["params"]["page"] == 1
        assert response == mock_response

    def test_get_request_raises_authentication_error_on_401(
        self, request_helper: RequestHelper, mock_session: MagicMock
    ) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_session.get.return_value = mock_response

        with pytest.raises(AuthenticationError) as exc_info:
            request_helper.get_request("/test")

        assert "Authentication failed" in exc_info.value.message
        assert exc_info.value.details["status_code"] == 401

    def test_get_request_raises_authentication_error_on_403(
        self, request_helper: RequestHelper, mock_session: MagicMock
    ) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_session.get.return_value = mock_response

        with pytest.raises(AuthenticationError) as exc_info:
            request_helper.get_request("/test")

        assert "Access forbidden" in exc_info.value.message
        assert exc_info.value.details["status_code"] == 403

    def test_get_request_raises_api_response_error_on_other_http_errors(
        self, request_helper: RequestHelper, mock_session: MagicMock
    ) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_session.get.return_value = mock_response

        with pytest.raises(APIResponseError) as exc_info:
            request_helper.get_request("/test")

        assert exc_info.value.status_code == 500

    def test_get_request_raises_esios_api_error_on_network_error(
        self, request_helper: RequestHelper, mock_session: MagicMock
    ) -> None:
        mock_session.get.side_effect = RequestException("Connection refused")

        with pytest.raises(ESIOSAPIError) as exc_info:
            request_helper.get_request("/test")

        assert "Network error" in exc_info.value.message

    def test_get_request_success(
        self, request_helper: RequestHelper, mock_session: MagicMock
    ) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = {"indicators": []}
        mock_session.get.return_value = mock_response

        response = request_helper.get_request("/indicators")

        assert response.json() == {"indicators": []}
        mock_session.get.assert_called_once()
