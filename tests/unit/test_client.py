import logging
import time
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from recruit_crm_mcp import client


def _make_response(status_code: int, headers: dict | None = None, json_body: dict | None = None) -> httpx.Response:
    """Build a fake httpx.Response for testing."""
    resp = httpx.Response(
        status_code=status_code,
        headers=headers or {},
        json=json_body or {},
        request=httpx.Request("GET", "https://api.recruitcrm.io/v1/test"),
    )
    return resp


class TestHeaders:
    def test_includes_bearer_token(self):
        headers = client._headers()
        assert headers["Authorization"] == "Bearer test-key-123"
        assert headers["Accept"] == "application/json"


class TestGetApiKey:
    def test_returns_key(self):
        assert client._get_api_key() == "test-key-123"

    def test_raises_without_key(self, monkeypatch):
        monkeypatch.delenv("RECRUIT_CRM_API_KEY")
        with pytest.raises(RuntimeError, match="RECRUIT_CRM_API_KEY"):
            client._get_api_key()


class TestFindCandidates:
    @pytest.mark.anyio
    async def test_with_filters_uses_search_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/candidates/search"
            return {"data": [{"first_name": "Jane", "last_name": "Doe"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_candidates(first_name="Jane")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_without_filters_uses_list_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/candidates"
            assert "per_page" in params
            return {"data": [{"first_name": "Jane"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_candidates()
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_passes_name_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/candidates/search"
            assert params["first_name"] == "Jane"
            assert params["last_name"] == "Doe"
            return {"data": [{"first_name": "Jane", "last_name": "Doe"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_candidates(first_name="Jane", last_name="Doe")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_passes_email_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/candidates/search"
            assert params["email"] == "jane@example.com"
            return {"data": [{"email": "jane@example.com"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_candidates(email="jane@example.com")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_passes_location_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/candidates/search"
            assert params["country"] == "US"
            assert params["state"] == "California"
            return {"data": [{"first_name": "Jane"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_candidates(country="US", state="California")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_enforces_limit_with_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": [{"id": i} for i in range(100)]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_candidates(first_name="Jane", limit=5)
        assert len(results) == 5

    @pytest.mark.anyio
    async def test_enforces_limit_without_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": [{"id": i} for i in range(100)]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_candidates(limit=3)
        assert len(results) == 3

    @pytest.mark.anyio
    async def test_handles_list_response(self, monkeypatch):
        async def mock_get(path, params=None):
            return [{"first_name": "Jane"}]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_candidates(first_name="Jane")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_handles_empty_response(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_candidates(first_name="nobody")
        assert results == []


class TestGetCandidate:
    @pytest.mark.anyio
    async def test_fetches_by_slug(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/candidates/jane-doe"
            return {"first_name": "Jane", "last_name": "Doe"}

        monkeypatch.setattr(client, "get", mock_get)
        result = await client.get_candidate("jane-doe")
        assert result["first_name"] == "Jane"


class TestGetJobStatusId:
    @pytest.mark.anyio
    async def test_resolves_label_to_id(self, monkeypatch):
        monkeypatch.setattr(client, "_job_statuses", None)

        async def mock_get(path, params=None):
            assert path == "/jobs-pipeline"
            return [{"id": 1, "label": "Open"}, {"id": 2, "label": "On Hold"}]

        monkeypatch.setattr(client, "get", mock_get)
        status_id = await client._get_job_status_id("Open")
        assert status_id == 1

    @pytest.mark.anyio
    async def test_case_insensitive(self, monkeypatch):
        monkeypatch.setattr(client, "_job_statuses", {"open": 1})
        status_id = await client._get_job_status_id("OPEN")
        assert status_id == 1

    @pytest.mark.anyio
    async def test_caches_after_first_fetch(self, monkeypatch):
        monkeypatch.setattr(client, "_job_statuses", None)
        call_count = 0

        async def mock_get(path, params=None):
            nonlocal call_count
            call_count += 1
            return [{"id": 1, "label": "Open"}]

        monkeypatch.setattr(client, "get", mock_get)
        await client._get_job_status_id("Open")
        await client._get_job_status_id("Open")
        assert call_count == 1

    @pytest.mark.anyio
    async def test_unknown_status_raises(self, monkeypatch):
        monkeypatch.setattr(client, "_job_statuses", {"open": 1})
        with pytest.raises(ValueError, match="Unknown job status"):
            await client._get_job_status_id("Bogus")

    @pytest.mark.anyio
    async def test_zero_id_status_raises(self, monkeypatch):
        monkeypatch.setattr(client, "_job_statuses", {"closed": 0, "open": 1})
        with pytest.raises(ValueError, match="Cannot filter by status"):
            await client._get_job_status_id("Closed")


class TestFindJobs:
    @pytest.mark.anyio
    async def test_without_filters_uses_list_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs"
            assert "per_page" in params
            return {"data": [{"name": "Engineer"}, {"name": "Designer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_jobs()
        assert len(results) == 2

    @pytest.mark.anyio
    async def test_with_name_uses_search_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            assert params["name"] == "Engineer"
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_jobs(name="Engineer")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_with_status_resolves_and_searches(self, monkeypatch):
        monkeypatch.setattr(client, "_job_statuses", {"open": 1})

        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            assert params["job_status"] == 1
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_jobs(status="Open")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_with_location_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            assert params["city"] == "Austin"
            assert params["country"] == "US"
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_jobs(city="Austin", country="US")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_with_company_name(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            assert params["company_name"] == "Acme"
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_jobs(company_name="Acme")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_enforces_limit(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": [{"id": i} for i in range(50)]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.find_jobs(limit=5)
        assert len(results) == 5


class TestGetJob:
    @pytest.mark.anyio
    async def test_fetches_by_slug(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/backend-eng"
            return {"name": "Backend Engineer"}

        monkeypatch.setattr(client, "get", mock_get)
        result = await client.get_job("backend-eng")
        assert result["name"] == "Backend Engineer"


class TestParseRetryAfter:
    def test_retry_after_header(self):
        resp = _make_response(429, headers={"Retry-After": "5"})
        assert client._parse_retry_after(resp) == 5.0

    def test_retry_after_decimal(self):
        resp = _make_response(429, headers={"Retry-After": "2.5"})
        assert client._parse_retry_after(resp) == 2.5

    def test_retry_after_capped_at_120(self):
        resp = _make_response(429, headers={"Retry-After": "3600"})
        assert client._parse_retry_after(resp) == 120.0

    def test_x_ratelimit_reset_header(self):
        future = time.time() + 30
        resp = _make_response(429, headers={"X-RateLimit-Reset": str(future)})
        wait = client._parse_retry_after(resp)
        assert 28 < wait <= 30

    def test_x_ratelimit_reset_in_past_falls_through(self):
        past = time.time() - 10
        resp = _make_response(429, headers={"X-RateLimit-Reset": str(past)})
        assert client._parse_retry_after(resp) == 10.0

    def test_x_ratelimit_reset_capped_at_120(self):
        future = time.time() + 999
        resp = _make_response(429, headers={"X-RateLimit-Reset": str(future)})
        assert client._parse_retry_after(resp) == 120.0

    def test_no_headers_returns_default(self):
        resp = _make_response(429)
        assert client._parse_retry_after(resp) == 10.0

    def test_invalid_retry_after_falls_through(self):
        resp = _make_response(429, headers={"Retry-After": "not-a-number"})
        assert client._parse_retry_after(resp) == 10.0


class TestRateLimitRetry:
    @pytest.mark.anyio
    async def test_retries_on_429_then_succeeds(self, monkeypatch):
        """First request returns 429, retry succeeds."""
        rate_limited = _make_response(429, headers={"Retry-After": "0"})
        success = _make_response(200, json_body={"data": "ok"})

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(side_effect=[rate_limited, success])
        monkeypatch.setattr(client, "_client", mock_client)

        with patch("recruit_crm_mcp.client.asyncio.sleep") as mock_sleep:
            result = await client.get("/test")

        mock_sleep.assert_called_once()
        assert result == {"data": "ok"}
        assert mock_client.get.call_count == 2

    @pytest.mark.anyio
    async def test_raises_on_second_429(self, monkeypatch):
        """Both requests return 429 — should raise HTTPStatusError."""
        rate_limited_1 = _make_response(429, headers={"Retry-After": "0"})
        rate_limited_2 = _make_response(429, headers={"Retry-After": "0"})

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(side_effect=[rate_limited_1, rate_limited_2])
        monkeypatch.setattr(client, "_client", mock_client)

        with patch("recruit_crm_mcp.client.asyncio.sleep"):
            with pytest.raises(httpx.HTTPStatusError):
                await client.get("/test")

    @pytest.mark.anyio
    async def test_no_retry_on_success(self, monkeypatch):
        """200 response goes straight through without retry."""
        success = _make_response(200, json_body={"ok": True})

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=success)
        monkeypatch.setattr(client, "_client", mock_client)

        result = await client.get("/test")
        assert result == {"ok": True}
        assert mock_client.get.call_count == 1

    @pytest.mark.anyio
    async def test_non_429_error_raises_immediately(self, monkeypatch):
        """500 error is not retried — raises immediately."""
        error_resp = _make_response(500)

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=error_resp)
        monkeypatch.setattr(client, "_client", mock_client)

        with pytest.raises(httpx.HTTPStatusError):
            await client.get("/test")
        assert mock_client.get.call_count == 1

    @pytest.mark.anyio
    async def test_logs_warning_on_429(self, monkeypatch, caplog):
        """Rate limit triggers a warning log message."""
        rate_limited = _make_response(429, headers={"Retry-After": "0"})
        success = _make_response(200, json_body={})

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(side_effect=[rate_limited, success])
        monkeypatch.setattr(client, "_client", mock_client)

        with patch("recruit_crm_mcp.client.asyncio.sleep"):
            with caplog.at_level(logging.WARNING, logger="recruit_crm_mcp.client"):
                await client.get("/candidates")

        assert "Rate limited" in caplog.text
        assert "/candidates" in caplog.text
