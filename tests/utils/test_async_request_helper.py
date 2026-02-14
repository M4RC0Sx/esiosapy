from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from esiosapy.exceptions import APIResponseError
from esiosapy.exceptions import AuthenticationError
from esiosapy.utils.async_request_helper import AsyncRequestHelper


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestAsyncRequestHelper:
    @pytest.fixture
    def async_request_helper(self, mocker: MockerFixture) -> AsyncRequestHelper:
        mocker.patch("esiosapy.utils.async_request_helper._HTTPX_AVAILABLE", True)
        helper = AsyncRequestHelper(
            base_url="https://api.example.com", token="test-token"
        )
        return helper

    def test_add_default_headers_with_empty_headers(
        self, async_request_helper: AsyncRequestHelper
    ) -> None:
        headers: dict[str, str] = {}
        expected_headers: dict[str, str] = {
            "Accept": "application/json; application/vnd.esios-api-v1+json",
            "Content-Type": "application/json",
            "x-api-key": "test-token",
            "User-Agent": "esiosapy/0.0.1",
        }

        result = async_request_helper.add_default_headers(headers)

        assert result == expected_headers

    def test_add_default_headers_with_existing_headers(
        self, async_request_helper: AsyncRequestHelper
    ) -> None:
        headers: dict[str, str] = {
            "Accept": "text/html",
            "Content-Type": "application/xml",
            "x-api-key": "another-token",
        }

        result = async_request_helper.add_default_headers(headers)

        assert result == headers

    @pytest.mark.asyncio
    async def test_get_request_success(
        self, async_request_helper: AsyncRequestHelper, mocker: MockerFixture
    ) -> None:
        import httpx

        mock_response = mocker.MagicMock(spec=httpx.Response)
        mock_response.json.return_value = {"data": "test"}
        mock_response.status_code = 200

        mock_client = mocker.MagicMock()
        mock_client.get = mocker.AsyncMock(return_value=mock_response)
        async_request_helper._client = mock_client

        await async_request_helper.get_request("/test")

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert "x-api-key" in call_args[1]["headers"]
        assert call_args[1]["headers"]["x-api-key"] == "test-token"

    @pytest.mark.asyncio
    async def test_get_request_with_custom_headers_and_params(
        self, async_request_helper: AsyncRequestHelper, mocker: MockerFixture
    ) -> None:
        import httpx

        mock_response = mocker.MagicMock(spec=httpx.Response)
        mock_response.json.return_value = {"data": "test"}
        mock_response.status_code = 200

        mock_client = mocker.MagicMock()
        mock_client.get = mocker.AsyncMock(return_value=mock_response)
        async_request_helper._client = mock_client

        await async_request_helper.get_request(
            "/test", headers={"Accept": "text/xml"}, params={"page": 1}
        )

        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert call_args[1]["headers"]["Accept"] == "text/xml"
        assert call_args[1]["params"]["page"] == 1

    @pytest.mark.asyncio
    async def test_get_request_raises_authentication_error_on_401(
        self, async_request_helper: AsyncRequestHelper, mocker: MockerFixture
    ) -> None:
        import httpx

        mock_response = mocker.MagicMock(spec=httpx.Response)
        mock_response.status_code = 401

        mock_client = mocker.MagicMock()
        mock_client.get = mocker.AsyncMock(
            side_effect=httpx.HTTPStatusError(
                message="Error", request=mocker.MagicMock(), response=mock_response
            )
        )
        async_request_helper._client = mock_client

        with pytest.raises(AuthenticationError) as exc_info:
            await async_request_helper.get_request("/test")

        assert "Authentication failed" in exc_info.value.message
        assert exc_info.value.details["status_code"] == 401

    @pytest.mark.asyncio
    async def test_get_request_raises_authentication_error_on_403(
        self, async_request_helper: AsyncRequestHelper, mocker: MockerFixture
    ) -> None:
        import httpx

        mock_response = mocker.MagicMock(spec=httpx.Response)
        mock_response.status_code = 403

        mock_client = mocker.MagicMock()
        mock_client.get = mocker.AsyncMock(
            side_effect=httpx.HTTPStatusError(
                message="Error", request=mocker.MagicMock(), response=mock_response
            )
        )
        async_request_helper._client = mock_client

        with pytest.raises(AuthenticationError) as exc_info:
            await async_request_helper.get_request("/test")

        assert "Access forbidden" in exc_info.value.message
        assert exc_info.value.details["status_code"] == 403

    @pytest.mark.asyncio
    async def test_get_request_raises_api_response_error_on_other_http_errors(
        self, async_request_helper: AsyncRequestHelper, mocker: MockerFixture
    ) -> None:
        import httpx

        mock_response = mocker.MagicMock(spec=httpx.Response)
        mock_response.status_code = 500

        mock_client = mocker.MagicMock()
        mock_client.get = mocker.AsyncMock(
            side_effect=httpx.HTTPStatusError(
                message="Error", request=mocker.MagicMock(), response=mock_response
            )
        )
        async_request_helper._client = mock_client

        with pytest.raises(APIResponseError) as exc_info:
            await async_request_helper.get_request("/test")

        assert exc_info.value.status_code == 500

    @pytest.mark.asyncio
    async def test_get_request_raises_api_error_on_network_error(
        self, async_request_helper: AsyncRequestHelper, mocker: MockerFixture
    ) -> None:
        import httpx

        mock_client = mocker.MagicMock()
        mock_client.get = mocker.AsyncMock(
            side_effect=httpx.ConnectError("Connection failed")
        )
        async_request_helper._client = mock_client

        with pytest.raises(Exception) as exc_info:
            await async_request_helper.get_request("/test")

        assert "Network error" in str(exc_info.value) or "ConnectError" in str(
            type(exc_info.value)
        )

    @pytest.mark.asyncio
    async def test_context_manager(
        self, async_request_helper: AsyncRequestHelper, mocker: MockerFixture
    ) -> None:
        import httpx

        mock_response = mocker.MagicMock(spec=httpx.Response)
        mock_response.json.return_value = {"data": "test"}
        mock_response.status_code = 200

        mock_client = mocker.MagicMock()
        mock_client.get = mocker.AsyncMock(return_value=mock_response)
        mock_client.aclose = mocker.AsyncMock()
        async_request_helper._client = mock_client

        async with async_request_helper as helper:
            assert helper is async_request_helper

        mock_client.aclose.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_without_context(
        self, async_request_helper: AsyncRequestHelper, mocker: MockerFixture
    ) -> None:

        mock_client = mocker.MagicMock()
        mock_client.aclose = mocker.AsyncMock()
        async_request_helper._client = mock_client

        await async_request_helper.close()

        mock_client.aclose.assert_called_once()
        assert async_request_helper._client is None


class TestAsyncRequestHelperImportError:
    def test_import_error_when_httpx_not_available(self, mocker: MockerFixture) -> None:
        mocker.patch("esiosapy.utils.async_request_helper._HTTPX_AVAILABLE", False)

        with pytest.raises(ImportError, match="httpx"):
            AsyncRequestHelper(base_url="https://api.example.com", token="test")
