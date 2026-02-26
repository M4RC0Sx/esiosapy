from __future__ import annotations

from typing import Any


class ESIOSAPIError(Exception):
    """Base exception for all ESIOS API errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AuthenticationError(ESIOSAPIError):
    """Raised when authentication fails (invalid or missing API token)."""


class APIResponseError(ESIOSAPIError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: str | None = None,
    ):
        super().__init__(
            message, {"status_code": status_code, "response_body": response_body}
        )
        self.status_code = status_code
        self.response_body = response_body
