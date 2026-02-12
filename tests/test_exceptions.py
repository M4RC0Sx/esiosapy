from __future__ import annotations

from esiosapy.exceptions import APIResponseError
from esiosapy.exceptions import AuthenticationError
from esiosapy.exceptions import ESIOSAPIError


class TestESIOSAPIError:
    def test_initialization_with_message(self) -> None:
        error = ESIOSAPIError("Test error message")
        assert error.message == "Test error message"
        assert error.details == {}
        assert str(error) == "Test error message"

    def test_initialization_with_message_and_details(self) -> None:
        details = {"status_code": 404, "extra": "info"}
        error = ESIOSAPIError("Test error", details=details)
        assert error.message == "Test error"
        assert error.details == details

    def test_details_default_empty_dict(self) -> None:
        error = ESIOSAPIError("Test")
        assert isinstance(error.details, dict)
        assert error.details == {}


class TestAuthenticationError:
    def test_inherits_from_esios_api_error(self) -> None:
        error = AuthenticationError("Auth failed")
        assert isinstance(error, ESIOSAPIError)

    def test_initialization(self) -> None:
        error = AuthenticationError("Invalid token")
        assert error.message == "Invalid token"


class TestAPIResponseError:
    def test_inherits_from_esios_api_error(self) -> None:
        error = APIResponseError("API error")
        assert isinstance(error, ESIOSAPIError)

    def test_initialization_with_status_code(self) -> None:
        error = APIResponseError("Not found", status_code=404)
        assert error.message == "Not found"
        assert error.status_code == 404

    def test_initialization_with_response_body(self) -> None:
        error = APIResponseError("Error", status_code=500, response_body="Server error")
        assert error.status_code == 500
        assert error.response_body == "Server error"

    def test_details_include_status_code(self) -> None:
        error = APIResponseError("Error", status_code=403)
        assert error.details["status_code"] == 403
