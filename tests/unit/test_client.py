import logging
import time
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from recruit_crm_mcp import client


def _make_response(
    status_code: int,
    headers: dict | None = None,
    json_body: dict | None = None,
    method: str = "GET",
    *,
    empty_body: bool = False,
) -> httpx.Response:
    """Build a fake httpx.Response for testing."""
    kwargs: dict = {
        "status_code": status_code,
        "headers": headers or {},
        "request": httpx.Request(method, "https://api.recruitcrm.io/v1/test"),
    }
    if empty_body:
        kwargs["content"] = b""
    else:
        kwargs["json"] = json_body or {}
    return httpx.Response(**kwargs)


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


class TestSearchCandidates:
    @pytest.mark.anyio
    async def test_email_uses_search_endpoint(self, monkeypatch):
        """Email filter should route to /candidates/search, not /candidates."""
        async def mock_get(path, params=None):
            assert path == "/candidates/search"
            assert params["email"] == "jane@example.com"
            return {"data": [{"email": "jane@example.com"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_candidates(email="jane@example.com")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_search_endpoint_does_not_send_per_page(self, monkeypatch):
        """The /candidates/search endpoint rejects per_page with 400."""
        async def mock_get(path, params=None):
            assert "per_page" not in params
            return {"data": [{"first_name": "Jane"}]}

        monkeypatch.setattr(client, "get", mock_get)
        await client.search_candidates(first_name="Jane")

    @pytest.mark.anyio
    async def test_first_name_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/candidates/search"
            assert params["first_name"] == "Jane"
            return {"data": [{"first_name": "Jane"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_candidates(first_name="Jane")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_last_name_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/candidates/search"
            assert params["last_name"] == "Doe"
            return {"data": [{"last_name": "Doe"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_candidates(last_name="Doe")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_no_filters_uses_list_endpoint(self, monkeypatch):
        """No filters should fall back to /candidates with limit only."""
        async def mock_get(path, params=None):
            assert path == "/candidates"
            assert "limit" in params
            assert "sort_by" not in params
            assert "sort_order" not in params
            assert "per_page" not in params
            return {"data": [{"first_name": "Jane"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_candidates()
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_combined_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/candidates/search"
            assert params["first_name"] == "Jane"
            assert params["last_name"] == "Doe"
            assert params["email"] == "jane@example.com"
            assert "per_page" not in params
            return {"data": [{"first_name": "Jane", "last_name": "Doe"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_candidates(
            first_name="Jane", last_name="Doe", email="jane@example.com"
        )
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_handles_list_response(self, monkeypatch):
        async def mock_get(path, params=None):
            return [{"first_name": "Jane"}]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_candidates(first_name="Jane")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_handles_empty_response(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_candidates(first_name="nobody")
        assert results == []

    @pytest.mark.anyio
    async def test_state_and_country_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/candidates/search"
            assert params["state"] == "California"
            assert params["country"] == "US"
            return {"data": [{"first_name": "Jane"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_candidates(state="California", country="US")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_date_range_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/candidates/search"
            assert params["created_from"] == "2025-01-01"
            assert params["created_to"] == "2025-06-30"
            assert params["updated_from"] == "2025-03-01"
            assert params["updated_to"] == "2025-06-30"
            return {"data": [{"first_name": "Jane"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_candidates(
            created_from="2025-01-01",
            created_to="2025-06-30",
            updated_from="2025-03-01",
            updated_to="2025-06-30",
        )
        assert len(results) == 1



class TestSearchContacts:
    @pytest.mark.anyio
    async def test_no_filters_uses_list_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/contacts"
            assert "limit" in params
            return {"data": [{"first_name": "Jane"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_contacts()
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_email_uses_search_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/contacts/search"
            assert params["email"] == "jane@example.com"
            return {"data": [{"email": "jane@example.com"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_contacts(email="jane@example.com")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_search_does_not_send_per_page(self, monkeypatch):
        async def mock_get(path, params=None):
            assert "per_page" not in params
            return {"data": [{"first_name": "Jane"}]}

        monkeypatch.setattr(client, "get", mock_get)
        await client.search_contacts(first_name="Jane")

    @pytest.mark.anyio
    async def test_company_slug_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/contacts/search"
            assert params["company_slug"] == "acme-corp"
            return {"data": [{"company_slug": "acme-corp"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_contacts(company_slug="acme-corp")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_owner_id_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/contacts/search"
            assert params["owner_id"] == 43135
            return {"data": [{"owner": 43135}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_contacts(owner_id=43135)
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_date_range_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/contacts/search"
            assert params["created_from"] == "2025-01-01"
            assert params["created_to"] == "2025-06-30"
            assert params["updated_from"] == "2025-03-01"
            assert params["updated_to"] == "2025-06-30"
            return {"data": [{"first_name": "Jane"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_contacts(
            created_from="2025-01-01",
            created_to="2025-06-30",
            updated_from="2025-03-01",
            updated_to="2025-06-30",
        )
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_enforces_limit_client_side(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": [{"id": i} for i in range(100)]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_contacts(limit=3)
        assert len(results) == 3

    @pytest.mark.anyio
    async def test_handles_empty_response(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_contacts(first_name="nobody")
        assert results == []


class TestGetContact:
    @pytest.mark.anyio
    async def test_fetches_by_slug(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/contacts/jane-doe"
            return {"first_name": "Jane", "last_name": "Doe"}

        monkeypatch.setattr(client, "get", mock_get)
        result = await client.get_contact("jane-doe")
        assert result["first_name"] == "Jane"


class TestSearchNotes:
    @pytest.mark.anyio
    async def test_uses_search_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/notes/search"
            assert params["added_from"] == "2025-01-01"
            return {"data": [{"id": 1}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_notes(added_from="2025-01-01")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_no_filters_uses_list_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/notes"
            assert "limit" in params
            return {"data": [{"id": 1}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_notes()
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_date_range_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/notes/search"
            assert params["added_from"] == "2025-01-01"
            assert params["added_to"] == "2025-06-30"
            assert params["updated_from"] == "2025-03-01"
            assert params["updated_to"] == "2025-06-30"
            return {"data": [{"id": 1}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_notes(
            added_from="2025-01-01",
            added_to="2025-06-30",
            updated_from="2025-03-01",
            updated_to="2025-06-30",
        )
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_enforces_limit_client_side(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": [{"id": i} for i in range(100)]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_notes(limit=3)
        assert len(results) == 3

    @pytest.mark.anyio
    async def test_handles_empty_response(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_notes(added_from="2099-01-01")
        assert results == []


class TestGetNote:
    @pytest.mark.anyio
    async def test_fetches_by_id(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/notes/12345"
            return {"id": 12345, "description": "A note"}

        monkeypatch.setattr(client, "get", mock_get)
        result = await client.get_note(12345)
        assert result["id"] == 12345


class TestSearchTasks:
    @pytest.mark.anyio
    async def test_uses_search_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/tasks/search"
            assert params["title"] == "Follow up"
            return {"data": [{"title": "Follow up"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_tasks(title="Follow up")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_no_filters_uses_list_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/tasks"
            assert "limit" in params
            return {"data": [{"title": "Task"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_tasks()
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_owner_id_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/tasks/search"
            assert params["owner_id"] == 43135
            return {"data": [{"owner": 43135}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_tasks(owner_id=43135)
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_date_range_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/tasks/search"
            assert params["created_from"] == "2025-01-01"
            assert params["created_to"] == "2025-06-30"
            assert params["updated_from"] == "2025-03-01"
            assert params["updated_to"] == "2025-06-30"
            return {"data": [{"title": "Task"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_tasks(
            created_from="2025-01-01",
            created_to="2025-06-30",
            updated_from="2025-03-01",
            updated_to="2025-06-30",
        )
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_starting_date_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/tasks/search"
            assert params["starting_from"] == "2025-01-01"
            assert params["starting_to"] == "2025-12-31"
            return {"data": [{"title": "Task"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_tasks(
            starting_from="2025-01-01",
            starting_to="2025-12-31",
        )
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_enforces_limit_client_side(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": [{"id": i} for i in range(100)]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_tasks(limit=3)
        assert len(results) == 3

    @pytest.mark.anyio
    async def test_handles_empty_response(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_tasks(title="nonexistent")
        assert results == []


class TestGetTask:
    @pytest.mark.anyio
    async def test_fetches_by_id(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/tasks/12345"
            return {"id": 12345, "title": "Follow up"}

        monkeypatch.setattr(client, "get", mock_get)
        result = await client.get_task(12345)
        assert result["id"] == 12345


class TestSearchCompanies:
    @pytest.mark.anyio
    async def test_uses_search_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/companies/search"
            assert params["company_name"] == "Acme"
            return {"data": [{"company_name": "Acme"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_companies(company_name="Acme")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_no_filters_uses_list_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/companies"
            assert "limit" in params
            return {"data": [{"company_name": "Acme"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_companies()
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_owner_id_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/companies/search"
            assert params["owner_id"] == 43135
            return {"data": [{"owner": 43135}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_companies(owner_id=43135)
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_date_range_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/companies/search"
            assert params["created_from"] == "2025-01-01"
            assert params["created_to"] == "2025-06-30"
            assert params["updated_from"] == "2025-03-01"
            assert params["updated_to"] == "2025-06-30"
            return {"data": [{"company_name": "Acme"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_companies(
            created_from="2025-01-01",
            created_to="2025-06-30",
            updated_from="2025-03-01",
            updated_to="2025-06-30",
        )
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_sort_params(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/companies/search"
            assert params["sort_by"] == "createdon"
            assert params["sort_order"] == "asc"
            return {"data": [{"company_name": "Acme"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_companies(
            company_name="Acme", sort_by="createdon", sort_order="asc",
        )
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_exact_search_sends_string(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/companies/search"
            assert params["exact_search"] == "true"
            return {"data": [{"company_name": "Acme"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_companies(
            company_name="Acme", exact_search=True,
        )
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_enforces_limit_client_side(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": [{"id": i} for i in range(100)]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_companies(limit=3)
        assert len(results) == 3

    @pytest.mark.anyio
    async def test_handles_empty_response(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_companies(company_name="nonexistent")
        assert results == []


class TestGetCompany:
    @pytest.mark.anyio
    async def test_fetches_by_slug(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/companies/acme-corp"
            return {"company_name": "Acme Corp", "slug": "acme-corp"}

        monkeypatch.setattr(client, "get", mock_get)
        result = await client.get_company("acme-corp")
        assert result["company_name"] == "Acme Corp"


class TestSearchMeetings:
    @pytest.mark.anyio
    async def test_uses_search_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/meetings/search"
            assert params["title"] == "Interview"
            return {"data": [{"title": "Interview"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_meetings(title="Interview")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_no_filters_uses_list_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/meetings"
            assert "limit" in params
            return {"data": [{"title": "Standup"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_meetings()
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_owner_id_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/meetings/search"
            assert params["owner_id"] == 43135
            return {"data": [{"owner": 43135}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_meetings(owner_id=43135)
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_date_range_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/meetings/search"
            assert params["created_from"] == "2025-01-01"
            assert params["created_to"] == "2025-06-30"
            assert params["updated_from"] == "2025-03-01"
            assert params["updated_to"] == "2025-06-30"
            return {"data": [{"title": "Meeting"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_meetings(
            created_from="2025-01-01",
            created_to="2025-06-30",
            updated_from="2025-03-01",
            updated_to="2025-06-30",
        )
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_starting_date_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/meetings/search"
            assert params["starting_from"] == "2025-01-01"
            assert params["starting_to"] == "2025-12-31"
            return {"data": [{"title": "Meeting"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_meetings(
            starting_from="2025-01-01",
            starting_to="2025-12-31",
        )
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_enforces_limit_client_side(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": [{"id": i} for i in range(100)]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_meetings(limit=3)
        assert len(results) == 3

    @pytest.mark.anyio
    async def test_handles_empty_response(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_meetings(title="nonexistent")
        assert results == []


class TestGetMeeting:
    @pytest.mark.anyio
    async def test_fetches_by_id(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/meetings/12345"
            return {"id": 12345, "title": "Interview"}

        monkeypatch.setattr(client, "get", mock_get)
        result = await client.get_meeting(12345)
        assert result["id"] == 12345


class TestGetCandidate:
    @pytest.mark.anyio
    async def test_fetches_by_slug(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/candidates/jane-doe"
            return {"first_name": "Jane", "last_name": "Doe"}

        monkeypatch.setattr(client, "get", mock_get)
        result = await client.get_candidate("jane-doe")
        assert result["first_name"] == "Jane"


class TestListJobs:
    @pytest.mark.anyio
    async def test_uses_list_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs"
            assert "per_page" in params
            return {"data": [{"name": "Engineer"}, {"name": "Designer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_jobs()
        assert len(results) == 2

    @pytest.mark.anyio
    async def test_enforces_limit_client_side(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": [{"id": i} for i in range(100)]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_jobs(limit=3)
        assert len(results) == 3


class TestSearchJobs:
    @pytest.mark.anyio
    async def test_uses_search_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_jobs(name="Engineer")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_maps_status_label_to_id(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            assert params["job_status"] == 1  # "Open" → 1
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_jobs(status="Open")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_status_case_insensitive(self, monkeypatch):
        async def mock_get(path, params=None):
            assert params["job_status"] == 0  # "closed" → 0
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        await client.search_jobs(status="closed")

    @pytest.mark.anyio
    async def test_invalid_status_raises(self):
        with pytest.raises(ValueError, match="Unknown job status"):
            await client.search_jobs(status="InvalidStatus")

    @pytest.mark.anyio
    async def test_passes_all_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            assert params["job_status"] == 1
            assert params["name"] == "Engineer"
            assert params["city"] == "Austin"
            assert params["country"] == "US"
            assert params["company_name"] == "Acme"
            # Search endpoint does not accept per_page
            assert "per_page" not in params
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_jobs(
            status="Open", name="Engineer", city="Austin",
            country="US", company_name="Acme",
        )
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_omits_none_filters(self, monkeypatch):
        async def mock_get(path, params=None):
            assert "job_status" not in params
            assert "name" not in params
            assert "per_page" not in params
            assert "created_from" not in params
            assert "owner_id" not in params
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_jobs()
        assert results == []

    @pytest.mark.anyio
    async def test_enforces_limit_client_side(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": [{"id": i} for i in range(100)]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_jobs(name="x", limit=5)
        assert len(results) == 5

    @pytest.mark.anyio
    async def test_created_from_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            assert params["created_from"] == "2025-01-01"
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_jobs(created_from="2025-01-01")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_created_to_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            assert params["created_to"] == "2025-12-31"
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_jobs(created_to="2025-12-31")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_updated_from_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            assert params["updated_from"] == "2025-06-01"
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_jobs(updated_from="2025-06-01")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_updated_to_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            assert params["updated_to"] == "2025-12-31"
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_jobs(updated_to="2025-12-31")
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_owner_id_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            assert params["owner_id"] == 43135
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_jobs(owner_id=43135)
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_date_and_owner_combined(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/search"
            assert params["created_from"] == "2025-01-01"
            assert params["owner_id"] == 43135
            assert "per_page" not in params
            return {"data": [{"name": "Engineer"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_jobs(
            created_from="2025-01-01", owner_id=43135,
        )
        assert len(results) == 1


class TestGetAssignedCandidates:
    @pytest.mark.anyio
    async def test_calls_correct_endpoint(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/job-slug-123/assigned-candidates"
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        await client.get_assigned_candidates("job-slug-123")

    @pytest.mark.anyio
    async def test_passes_status_id_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert params["status_id"] == "5"
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        await client.get_assigned_candidates("job-slug-123", status_id="5")

    @pytest.mark.anyio
    async def test_passes_limit(self, monkeypatch):
        async def mock_get(path, params=None):
            assert params["limit"] == 10
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        await client.get_assigned_candidates("job-slug-123", limit=10)

    @pytest.mark.anyio
    async def test_enforces_limit_client_side(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": [{"candidate": {"id": i}, "status": {}} for i in range(50)]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.get_assigned_candidates("job-slug-123", limit=3)
        assert len(results) == 3


class TestGetJob:
    @pytest.mark.anyio
    async def test_fetches_by_slug(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/jobs/backend-eng"
            return {"name": "Backend Engineer"}

        monkeypatch.setattr(client, "get", mock_get)
        result = await client.get_job("backend-eng")
        assert result["name"] == "Backend Engineer"


class TestListUsers:
    @pytest.mark.anyio
    async def test_returns_users_from_data_key(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/users"
            return {"data": [
                {"id": 1, "first_name": "Jane", "last_name": "Doe"},
                {"id": 2, "first_name": "John", "last_name": "Smith"},
            ]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_users()
        assert len(results) == 2
        assert results[0]["first_name"] == "Jane"

    @pytest.mark.anyio
    async def test_handles_list_response(self, monkeypatch):
        async def mock_get(path, params=None):
            return [{"id": 1, "first_name": "Jane"}]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_users()
        assert len(results) == 1

    @pytest.mark.anyio
    async def test_handles_empty_response(self, monkeypatch):
        async def mock_get(path, params=None):
            return {"data": []}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_users()
        assert results == []


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
        mock_client.request = AsyncMock(side_effect=[rate_limited, success])
        monkeypatch.setattr(client, "_client", mock_client)

        with patch("recruit_crm_mcp.client.anyio.sleep") as mock_sleep:
            result = await client.get("/test")

        mock_sleep.assert_called_once()
        assert result == {"data": "ok"}
        assert mock_client.request.call_count == 2

    @pytest.mark.anyio
    async def test_raises_on_second_429(self, monkeypatch):
        """Both requests return 429 — should raise RecruitCrmError."""
        rate_limited_1 = _make_response(429, headers={"Retry-After": "0"})
        rate_limited_2 = _make_response(429, headers={"Retry-After": "0"})

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=[rate_limited_1, rate_limited_2])
        monkeypatch.setattr(client, "_client", mock_client)

        with patch("recruit_crm_mcp.client.anyio.sleep"):
            with pytest.raises(client.RecruitCrmError):
                await client.get("/test")

    @pytest.mark.anyio
    async def test_no_retry_on_success(self, monkeypatch):
        """200 response goes straight through without retry."""
        success = _make_response(200, json_body={"ok": True})

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=success)
        monkeypatch.setattr(client, "_client", mock_client)

        result = await client.get("/test")
        assert result == {"ok": True}
        assert mock_client.request.call_count == 1

    @pytest.mark.anyio
    async def test_non_429_error_raises_immediately(self, monkeypatch):
        """500 error is not retried — raises immediately."""
        error_resp = _make_response(500)

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=error_resp)
        monkeypatch.setattr(client, "_client", mock_client)

        with pytest.raises(client.RecruitCrmError):
            await client.get("/test")
        assert mock_client.request.call_count == 1

    @pytest.mark.anyio
    async def test_logs_warning_on_429(self, monkeypatch, caplog):
        """Rate limit triggers a warning log message."""
        rate_limited = _make_response(429, headers={"Retry-After": "0"})
        success = _make_response(200, json_body={})

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=[rate_limited, success])
        monkeypatch.setattr(client, "_client", mock_client)

        with patch("recruit_crm_mcp.client.anyio.sleep"):
            with caplog.at_level(logging.WARNING, logger="recruit_crm_mcp.client"):
                await client.get("/candidates")

        assert "Rate limited" in caplog.text
        assert "/candidates" in caplog.text


class TestRequestBase:
    """Tests for the shared _request() base method."""

    @pytest.mark.anyio
    async def test_get_request_sends_auth_headers(self, monkeypatch):
        """GET request includes Bearer token and Accept header."""
        success = _make_response(200, json_body={"ok": True})
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=success)
        monkeypatch.setattr(client, "_client", mock_client)

        await client._request("GET", "/test")

        call_kwargs = mock_client.request.call_args
        headers = call_kwargs.kwargs.get("headers") or call_kwargs[1].get("headers")
        assert headers["Authorization"] == "Bearer test-key-123"
        assert headers["Accept"] == "application/json"

    @pytest.mark.anyio
    async def test_post_request_sends_json_body(self, monkeypatch):
        """POST request sends data as JSON body."""
        success = _make_response(200, json_body={"id": 1}, method="POST")
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=success)
        monkeypatch.setattr(client, "_client", mock_client)

        await client._request("POST", "/candidates", data={"first_name": "Jane"})

        call_kwargs = mock_client.request.call_args
        assert call_kwargs.kwargs.get("json") == {"first_name": "Jane"}

    @pytest.mark.anyio
    async def test_rejects_data_and_files_together(self, monkeypatch):
        """Passing both JSON data and multipart files is a misuse — httpx
        auto-sets Content-Type from the body shape, so the two are mutually
        exclusive. Fail loudly instead of silently dropping ``data``."""
        # No client needed — the guard fires before any HTTP call.
        with pytest.raises(ValueError, match="mutually exclusive"):
            await client._request("POST", "/x", data={"a": 1}, files={"f": ("n", b"")})

    @pytest.mark.anyio
    async def test_delete_request_uses_delete_method(self, monkeypatch):
        """DELETE request uses correct HTTP method."""
        success = _make_response(200, method="DELETE", empty_body=True)
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=success)
        monkeypatch.setattr(client, "_client", mock_client)

        await client._request("DELETE", "/candidates/slug-123")

        call_args = mock_client.request.call_args
        assert call_args[0][0] == "DELETE"

    @pytest.mark.anyio
    async def test_retries_on_429_then_succeeds(self, monkeypatch):
        """First request returns 429, retry succeeds."""
        rate_limited = _make_response(429, headers={"Retry-After": "0"})
        success = _make_response(200, json_body={"data": "ok"})

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=[rate_limited, success])
        monkeypatch.setattr(client, "_client", mock_client)

        with patch("recruit_crm_mcp.client.anyio.sleep") as mock_sleep:
            result = await client._request("GET", "/test")

        mock_sleep.assert_called_once()
        assert result == {"data": "ok"}
        assert mock_client.request.call_count == 2

    @pytest.mark.anyio
    async def test_raises_on_second_429(self, monkeypatch):
        """Both requests return 429 — raises RecruitCrmError."""
        rate_limited_1 = _make_response(429, headers={"Retry-After": "0"})
        rate_limited_2 = _make_response(429, headers={"Retry-After": "0"})

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=[rate_limited_1, rate_limited_2])
        monkeypatch.setattr(client, "_client", mock_client)

        with patch("recruit_crm_mcp.client.anyio.sleep"):
            with pytest.raises(client.RecruitCrmError):
                await client._request("POST", "/test", data={"x": 1})

    @pytest.mark.anyio
    async def test_logs_warning_on_429(self, monkeypatch, caplog):
        """Rate limit triggers a warning log message."""
        rate_limited = _make_response(429, headers={"Retry-After": "0"})
        success = _make_response(200, json_body={})

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=[rate_limited, success])
        monkeypatch.setattr(client, "_client", mock_client)

        with patch("recruit_crm_mcp.client.anyio.sleep"):
            with caplog.at_level(logging.WARNING, logger="recruit_crm_mcp.client"):
                await client._request("GET", "/candidates")

        assert "Rate limited" in caplog.text
        assert "/candidates" in caplog.text

    @pytest.mark.anyio
    async def test_raises_on_500_immediately(self, monkeypatch):
        """500 error is not retried — raises immediately."""
        error_resp = _make_response(500)

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=error_resp)
        monkeypatch.setattr(client, "_client", mock_client)

        with pytest.raises(client.RecruitCrmError):
            await client._request("GET", "/test")
        assert mock_client.request.call_count == 1


class TestPost:
    """Tests for the post() convenience method."""

    @pytest.mark.anyio
    async def test_sends_json_body(self, monkeypatch):
        """POST body is forwarded as JSON."""
        success = _make_response(200, json_body={"id": 42, "first_name": "Jane"}, method="POST")
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=success)
        monkeypatch.setattr(client, "_client", mock_client)

        result = await client.post("/candidates", data={"first_name": "Jane"})

        call_kwargs = mock_client.request.call_args
        assert call_kwargs.kwargs.get("json") == {"first_name": "Jane"}
        assert result["first_name"] == "Jane"

    @pytest.mark.anyio
    async def test_returns_json_response(self, monkeypatch):
        """Response JSON is parsed and returned."""
        success = _make_response(200, json_body={"id": 1, "slug": "abc"}, method="POST")
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=success)
        monkeypatch.setattr(client, "_client", mock_client)

        result = await client.post("/notes", data={"description": "test"})
        assert result == {"id": 1, "slug": "abc"}

    @pytest.mark.anyio
    async def test_passes_query_params(self, monkeypatch):
        """Query params are forwarded on POST."""
        success = _make_response(200, json_body={"ok": True}, method="POST")
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=success)
        monkeypatch.setattr(client, "_client", mock_client)

        await client.post("/test", data={"x": 1}, params={"foo": "bar"})

        call_kwargs = mock_client.request.call_args
        assert call_kwargs.kwargs.get("params") == {"foo": "bar"}

    @pytest.mark.anyio
    async def test_retries_on_429(self, monkeypatch):
        """Rate limit retry works for POST."""
        rate_limited = _make_response(429, headers={"Retry-After": "0"}, method="POST")
        success = _make_response(200, json_body={"id": 1}, method="POST")

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=[rate_limited, success])
        monkeypatch.setattr(client, "_client", mock_client)

        with patch("recruit_crm_mcp.client.anyio.sleep"):
            result = await client.post("/candidates", data={"first_name": "Jane"})

        assert result == {"id": 1}
        assert mock_client.request.call_count == 2


class TestDelete:
    """Tests for the delete() convenience method."""

    @pytest.mark.anyio
    async def test_calls_correct_endpoint(self, monkeypatch):
        """DELETE request targets the correct path."""
        success = _make_response(200, method="DELETE", empty_body=True)
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=success)
        monkeypatch.setattr(client, "_client", mock_client)

        await client.delete("/candidates/slug-123")

        call_args = mock_client.request.call_args
        assert call_args[0][0] == "DELETE"
        assert "candidates/slug-123" in call_args[0][1]

    @pytest.mark.anyio
    async def test_handles_empty_response_body(self, monkeypatch):
        """200 with no JSON body returns None."""
        success = _make_response(200, method="DELETE", empty_body=True)
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=success)
        monkeypatch.setattr(client, "_client", mock_client)

        result = await client.delete("/candidates/slug-123")
        assert result is None

    @pytest.mark.anyio
    async def test_handles_json_response(self, monkeypatch):
        """200 with JSON body returns parsed JSON."""
        success = _make_response(200, json_body={"deleted": True}, method="DELETE")
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=success)
        monkeypatch.setattr(client, "_client", mock_client)

        result = await client.delete("/notes/123")
        assert result == {"deleted": True}

    @pytest.mark.anyio
    async def test_retries_on_429(self, monkeypatch):
        """Rate limit retry works for DELETE."""
        rate_limited = _make_response(429, headers={"Retry-After": "0"}, method="DELETE")
        success = _make_response(200, method="DELETE", empty_body=True)

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=[rate_limited, success])
        monkeypatch.setattr(client, "_client", mock_client)

        with patch("recruit_crm_mcp.client.anyio.sleep"):
            result = await client.delete("/candidates/slug-123")

        assert result is None
        assert mock_client.request.call_count == 2


class TestRecruitCrmError:
    """Tests for the structured RecruitCrmError raised on non-2xx responses."""

    @pytest.mark.anyio
    async def test_400_with_json_body(self, monkeypatch):
        """400 with JSON body exposes parsed dict on .body."""
        error_body = {"message": "Validation failed", "errors": {"title": ["required"]}}
        error_resp = _make_response(400, json_body=error_body)
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=error_resp)
        monkeypatch.setattr(client, "_client", mock_client)

        with pytest.raises(client.RecruitCrmError) as exc_info:
            await client._request("POST", "/notes", data={"x": 1})

        assert exc_info.value.status == 400
        assert exc_info.value.body == error_body

    @pytest.mark.anyio
    async def test_422_with_plain_text_body(self, monkeypatch):
        """422 with a non-JSON body falls back to the response text."""
        text_body = "Unprocessable Entity"
        error_resp = httpx.Response(
            status_code=422,
            headers={"content-type": "text/plain"},
            content=text_body.encode(),
            request=httpx.Request("POST", "https://api.recruitcrm.io/v1/test"),
        )
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=error_resp)
        monkeypatch.setattr(client, "_client", mock_client)

        with pytest.raises(client.RecruitCrmError) as exc_info:
            await client._request("POST", "/notes", data={"x": 1})

        assert exc_info.value.status == 422
        assert exc_info.value.body == text_body

    @pytest.mark.anyio
    async def test_500_with_empty_body(self, monkeypatch):
        """500 with an empty body sets .body to None."""
        error_resp = httpx.Response(
            status_code=500,
            headers={},
            content=b"",
            request=httpx.Request("GET", "https://api.recruitcrm.io/v1/test"),
        )
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=error_resp)
        monkeypatch.setattr(client, "_client", mock_client)

        with pytest.raises(client.RecruitCrmError) as exc_info:
            await client._request("GET", "/notes")

        assert exc_info.value.status == 500
        assert exc_info.value.body is None

    @pytest.mark.anyio
    async def test_error_message_includes_method_and_path(self, monkeypatch):
        """str(error) includes the HTTP method and path for debugging."""
        error_resp = _make_response(400, json_body={"msg": "bad"})
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=error_resp)
        monkeypatch.setattr(client, "_client", mock_client)

        with pytest.raises(client.RecruitCrmError) as exc_info:
            await client._request("POST", "/notes", data={"x": 1})

        message = str(exc_info.value)
        assert "POST" in message
        assert "/notes" in message
        assert exc_info.value.method == "POST"
        assert exc_info.value.path == "/notes"


class TestJoin:
    """Tests for the _join helper."""

    def test_empty_list_returns_none(self):
        assert client._join([]) is None

    def test_none_returns_none(self):
        assert client._join(None) is None

    def test_single_value(self):
        assert client._join(["a"]) == "a"

    def test_multiple_values(self):
        assert client._join(["a", "b", "c"]) == "a,b,c"


class TestListNoteTypes:
    @pytest.mark.anyio
    async def test_happy_path(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/note-types"
            return [{"id": 1, "label": "Note"}, {"id": 2, "label": "Call"}]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_note_types()
        assert len(results) == 2
        assert results[0]["id"] == 1
        assert results[0]["label"] == "Note"


class TestListMeetingTypes:
    @pytest.mark.anyio
    async def test_happy_path(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/meeting-types"
            return [{"id": 1, "label": "Client Meeting"}]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_meeting_types()
        assert len(results) == 1
        assert results[0]["label"] == "Client Meeting"


class TestListTaskTypes:
    @pytest.mark.anyio
    async def test_happy_path(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/task-types"
            return [{"id": 1, "label": "Follow up"}]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_task_types()
        assert len(results) == 1
        assert results[0]["label"] == "Follow up"


class TestListHiringPipelines:
    @pytest.mark.anyio
    async def test_maps_name_to_label(self, monkeypatch):
        """API returns {id, name} — we normalize name → label."""
        async def mock_get(path, params=None):
            assert path == "/hiring-pipelines"
            return [{"id": 0, "name": "Master Hiring Pipeline"}]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_hiring_pipelines()
        assert len(results) == 1
        assert results[0]["id"] == 0
        assert results[0]["label"] == "Master Hiring Pipeline"


class TestListHiringPipelineStages:
    @pytest.mark.anyio
    async def test_passes_pipeline_id_in_url(self, monkeypatch):
        """The pipeline_id must appear in the URL path."""
        async def mock_get(path, params=None):
            assert path == "/hiring-pipelines/7"
            return [{"status_id": 56, "label": "Lead"}]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_hiring_pipeline_stages(7)
        assert len(results) == 1
        assert results[0]["id"] == 56
        assert results[0]["label"] == "Lead"

    @pytest.mark.anyio
    async def test_master_pipeline_id_zero(self, monkeypatch):
        """pipeline_id=0 targets the master hiring pipeline."""
        async def mock_get(path, params=None):
            assert path == "/hiring-pipelines/0"
            return [{"status_id": 1, "label": "Applied"}]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_hiring_pipeline_stages(0)
        assert results[0]["id"] == 1


class TestListContactStages:
    @pytest.mark.anyio
    async def test_maps_stage_id_to_id(self, monkeypatch):
        """API returns {stage_id, label} — we normalize stage_id → id."""
        async def mock_get(path, params=None):
            assert path == "/sales-pipeline"
            return [{"stage_id": 56, "label": "Lead"}]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_contact_stages()
        assert len(results) == 1
        assert results[0]["id"] == 56
        assert results[0]["label"] == "Lead"


class TestListIndustries:
    @pytest.mark.anyio
    async def test_maps_industry_id_to_id(self, monkeypatch):
        """API returns {industry_id, label} — we normalize industry_id → id."""
        async def mock_get(path, params=None):
            assert path == "/industries"
            return [{"industry_id": 6, "label": "Apparel and Fashion"}]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_industries()
        assert len(results) == 1
        assert results[0]["id"] == 6
        assert results[0]["label"] == "Apparel and Fashion"


class TestListCompanyCustomFields:
    @pytest.mark.anyio
    async def test_maps_field_id_and_field_name(self, monkeypatch):
        """Custom fields use field_id/field_name — normalize to id/label, keep extras."""
        async def mock_get(path, params=None):
            assert path == "/custom-fields/companies"
            return [
                {
                    "field_id": 1,
                    "entity_type": "company",
                    "field_name": "Revenue",
                    "field_type": "text",
                    "default_value": None,
                },
            ]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_company_custom_fields()
        assert len(results) == 1
        assert results[0]["id"] == 1
        assert results[0]["label"] == "Revenue"
        # Extra fields preserved
        assert results[0]["field_type"] == "text"
        assert results[0]["entity_type"] == "company"


class TestListContactCustomFields:
    @pytest.mark.anyio
    async def test_maps_field_id_and_field_name(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/custom-fields/contacts"
            return [
                {
                    "field_id": 2,
                    "entity_type": "contact",
                    "field_name": "Hobbies",
                    "field_type": "text",
                },
            ]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_contact_custom_fields()
        assert len(results) == 1
        assert results[0]["id"] == 2
        assert results[0]["label"] == "Hobbies"
        assert results[0]["field_type"] == "text"


class TestListJobCustomFields:
    @pytest.mark.anyio
    async def test_maps_field_id_and_field_name(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/custom-fields/jobs"
            return [
                {
                    "field_id": 3,
                    "entity_type": "job",
                    "field_name": "Priority",
                    "field_type": "select",
                },
            ]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_job_custom_fields()
        assert len(results) == 1
        assert results[0]["id"] == 3
        assert results[0]["label"] == "Priority"
        assert results[0]["field_type"] == "select"


class TestListCandidateCustomFields:
    @pytest.mark.anyio
    async def test_maps_field_id_and_field_name(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/custom-fields/candidates"
            return [
                {
                    "field_id": 4,
                    "entity_type": "candidate",
                    "field_name": "GitHub",
                    "field_type": "url",
                },
            ]

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.list_candidate_custom_fields()
        assert len(results) == 1
        assert results[0]["id"] == 4
        assert results[0]["label"] == "GitHub"
        assert results[0]["field_type"] == "url"


class TestCreateMeeting:
    @pytest.mark.anyio
    async def test_posts_to_meetings_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"id": 1, "title": "Intro"}

        monkeypatch.setattr(client, "post", mock_post)
        payload = {"title": "Intro", "start_date": "2025-04-29T18:30:00Z"}
        result = await client.create_meeting(payload)

        assert captured["path"] == "/meetings"
        assert captured["data"] == payload
        assert result["id"] == 1

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        assert await client.create_meeting({"title": "x"}) == {}


class TestCreateNote:
    @pytest.mark.anyio
    async def test_posts_to_notes_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"id": 7}

        monkeypatch.setattr(client, "post", mock_post)
        payload = {"description": "hi", "related_to": "cand-1", "related_to_type": "candidate"}
        result = await client.create_note(payload)

        assert captured["path"] == "/notes"
        assert captured["data"] == payload
        assert result["id"] == 7


class TestCreateTask:
    @pytest.mark.anyio
    async def test_posts_to_tasks_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"id": 9, "title": "Follow up"}

        monkeypatch.setattr(client, "post", mock_post)
        payload = {"title": "Follow up", "start_date": "2025-05-01T09:00:00Z", "reminder": 1440}
        result = await client.create_task(payload)

        assert captured["path"] == "/tasks"
        assert captured["data"] == payload
        assert result["id"] == 9


class TestUpdateTask:
    @pytest.mark.anyio
    async def test_partial_post_to_task_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"id": 42, "title": data.get("title")}

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_task(42, {"title": "new title"})

        assert captured["path"] == "/tasks/42"
        assert captured["data"] == {"title": "new title"}
        assert result["id"] == 42

    @pytest.mark.anyio
    async def test_drops_none_values_from_patch(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["data"] = data
            return {"id": 1}

        monkeypatch.setattr(client, "post", mock_post)
        await client.update_task(1, {"title": "x", "description": None, "reminder": -1})

        assert captured["data"] == {"title": "x", "reminder": -1}
        assert "description" not in captured["data"]

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_task(1, {"title": "x"})
        assert result == {}


class TestCreateCompany:
    @pytest.mark.anyio
    async def test_posts_to_companies_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"slug": "acme", "company_name": "Acme"}

        monkeypatch.setattr(client, "post", mock_post)
        payload = {"company_name": "Acme", "city": "NYC"}
        result = await client.create_company(payload)

        assert captured["path"] == "/companies"
        assert captured["data"] == payload
        assert result["slug"] == "acme"

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        assert await client.create_company({"company_name": "x"}) == {}


class TestUpdateCompany:
    @pytest.mark.anyio
    async def test_partial_post_to_company_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"slug": "acme", "city": data.get("city")}

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_company("acme", {"city": "Boston"})

        assert captured["path"] == "/companies/acme"
        assert captured["data"] == {"city": "Boston"}
        assert result["city"] == "Boston"

    @pytest.mark.anyio
    async def test_drops_none_values_from_patch(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["data"] = data
            return {"slug": "acme"}

        monkeypatch.setattr(client, "post", mock_post)
        await client.update_company("acme", {"city": "Boston", "address": None})

        assert captured["data"] == {"city": "Boston"}
        assert "address" not in captured["data"]

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_company("acme", {"city": "x"})
        assert result == {}


class TestCreateContact:
    @pytest.mark.anyio
    async def test_posts_to_contacts_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"slug": "jdoe"}

        monkeypatch.setattr(client, "post", mock_post)
        payload = {"first_name": "Jane", "last_name": "Doe"}
        result = await client.create_contact(payload)

        assert captured["path"] == "/contacts"
        assert captured["data"] == payload
        assert result["slug"] == "jdoe"

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        assert await client.create_contact({"first_name": "x", "last_name": "y"}) == {}


class TestUpdateContact:
    @pytest.mark.anyio
    async def test_partial_post_to_contact_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"slug": "jdoe", "email": data.get("email")}

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_contact("jdoe", {"email": "j@x.com"})

        assert captured["path"] == "/contacts/jdoe"
        assert captured["data"] == {"email": "j@x.com"}
        assert result["email"] == "j@x.com"

    @pytest.mark.anyio
    async def test_drops_none_values_from_patch(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["data"] = data
            return {"slug": "jdoe"}

        monkeypatch.setattr(client, "post", mock_post)
        await client.update_contact("jdoe", {"email": "j@x.com", "city": None})

        assert captured["data"] == {"email": "j@x.com"}
        assert "city" not in captured["data"]

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_contact("jdoe", {"email": "x"})
        assert result == {}


class TestCreateJob:
    @pytest.mark.anyio
    async def test_posts_to_jobs_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"slug": "job-1", "name": "Eng"}

        monkeypatch.setattr(client, "post", mock_post)
        payload = {
            "name": "Eng",
            "company_slug": "acme",
            "contact_slug": "jdoe",
            "number_of_openings": 1,
            "currency_id": 1,
            "enable_job_application_form": 0,
            "job_description_text": "<p>hi</p>",
        }
        result = await client.create_job(payload)

        assert captured["path"] == "/jobs"
        assert captured["data"] == payload
        assert result["slug"] == "job-1"

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        assert await client.create_job({"name": "x"}) == {}


class TestUpdateJob:
    @pytest.mark.anyio
    async def test_partial_post_to_job_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"slug": "job-1", "job_status": data.get("job_status")}

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_job("job-1", {"job_status": 2})

        assert captured["path"] == "/jobs/job-1"
        assert captured["data"] == {"job_status": 2}
        assert result["job_status"] == 2

    @pytest.mark.anyio
    async def test_drops_none_values_from_patch(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["data"] = data
            return {"slug": "job-1"}

        monkeypatch.setattr(client, "post", mock_post)
        await client.update_job("job-1", {"job_status": 2, "name": None})

        assert captured["data"] == {"job_status": 2}
        assert "name" not in captured["data"]

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_job("job-1", {"job_status": 2})
        assert result == {}


class TestCreateCandidate:
    @pytest.mark.anyio
    async def test_posts_to_candidates_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"slug": "cand-1", "first_name": "Jane"}

        monkeypatch.setattr(client, "post", mock_post)
        payload = {"first_name": "Jane"}
        result = await client.create_candidate(payload)

        assert captured["path"] == "/candidates"
        assert captured["data"] == payload
        assert result["slug"] == "cand-1"

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        assert await client.create_candidate({"first_name": "x"}) == {}


class TestUpdateCandidate:
    @pytest.mark.anyio
    async def test_partial_post_to_candidate_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"slug": "cand-1", "position": data.get("position")}

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_candidate("cand-1", {"position": "Engineer"})

        assert captured["path"] == "/candidates/cand-1"
        assert captured["data"] == {"position": "Engineer"}
        assert result["position"] == "Engineer"

    @pytest.mark.anyio
    async def test_drops_none_values_from_patch(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["data"] = data
            return {"slug": "cand-1"}

        monkeypatch.setattr(client, "post", mock_post)
        await client.update_candidate("cand-1", {"position": "Engineer", "city": None})

        assert captured["data"] == {"position": "Engineer"}
        assert "city" not in captured["data"]

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_candidate("cand-1", {"position": "x"})
        assert result == {}


class TestUpdateMeeting:
    @pytest.mark.anyio
    async def test_partial_post_to_meeting_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            return {"id": 7, "title": data.get("title")}

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_meeting(7, {"title": "Updated"})

        assert captured["path"] == "/meetings/7"
        assert captured["data"] == {"title": "Updated"}
        assert result["title"] == "Updated"

    @pytest.mark.anyio
    async def test_drops_none_values_from_patch(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["data"] = data
            return {"id": 7}

        monkeypatch.setattr(client, "post", mock_post)
        await client.update_meeting(7, {"title": "Updated", "description": None})

        assert captured["data"] == {"title": "Updated"}
        assert "description" not in captured["data"]

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_meeting(1, {"title": "x"})
        assert result == {}


class TestDeleteNote:
    @pytest.mark.anyio
    async def test_calls_delete_with_notes_path(self, monkeypatch):
        captured: dict = {}

        async def mock_delete(path, params=None):
            captured["path"] = path
            captured["params"] = params
            return None

        monkeypatch.setattr(client, "delete", mock_delete)
        result = await client.delete_note(42)

        assert captured["path"] == "/notes/42"
        assert result is None


class TestAssignCandidate:
    @pytest.mark.anyio
    async def test_posts_with_job_slug_as_query_param(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            captured["params"] = params
            return {"candidate_slug": "cand-1", "shared_list_url": "https://..."}

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.assign_candidate("cand-1", "job-1")

        assert captured["path"] == "/candidates/cand-1/assign"
        assert captured["params"] == {"job_slug": "job-1"}
        # Body MUST NOT carry job_slug — the API expects it as a query param only
        assert captured["data"] is None
        assert result["candidate_slug"] == "cand-1"

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        assert await client.assign_candidate("cand-1", "job-1") == {}


class TestUnassignCandidate:
    @pytest.mark.anyio
    async def test_posts_with_job_slug_as_query_param(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            captured["params"] = params
            return {"candidate_slug": "cand-1"}

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.unassign_candidate("cand-1", "job-1")

        assert captured["path"] == "/candidates/cand-1/unassign"
        assert captured["params"] == {"job_slug": "job-1"}
        assert captured["data"] is None
        assert result["candidate_slug"] == "cand-1"

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        assert await client.unassign_candidate("cand-1", "job-1") == {}


class TestUpdateHiringStage:
    @pytest.mark.anyio
    async def test_both_slugs_in_path_and_body_forwarded(self, monkeypatch):
        captured: dict = {}

        async def mock_post(path, data=None, params=None):
            captured["path"] = path
            captured["data"] = data
            captured["params"] = params
            return {"candidate_slug": "cand-1", "status_id": data["status_id"]}

        monkeypatch.setattr(client, "post", mock_post)
        body = {"status_id": 5, "remark": "phone screen passed"}
        result = await client.update_hiring_stage("cand-1", "job-1", body)

        # Note the plural "hiring-stages" and both slugs in the path
        assert captured["path"] == "/candidates/cand-1/hiring-stages/job-1"
        assert captured["data"] == body
        assert captured["params"] is None
        assert result["status_id"] == 5

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_returns_none(self, monkeypatch):
        async def mock_post(path, data=None, params=None):
            return None

        monkeypatch.setattr(client, "post", mock_post)
        result = await client.update_hiring_stage("cand-1", "job-1", {"status_id": 1})
        assert result == {}


class TestUploadFile:
    @pytest.mark.anyio
    async def test_posts_multipart_to_files_endpoint(self, monkeypatch):
        captured: dict = {}

        async def mock_post_multipart(path, form, files, params=None):
            captured["path"] = path
            captured["form"] = form
            captured["files"] = files
            captured["params"] = params
            return {"file_link": "https://cdn/x.pdf", "file_name": "x.pdf"}

        monkeypatch.setattr(client, "post_multipart", mock_post_multipart)
        result = await client.upload_file(
            file_url="https://example.com/resume.pdf",
            related_to="cand-1",
            related_to_type="candidate",
            folder="Resumes",
        )

        assert captured["path"] == "/files"
        assert captured["form"] == {
            "related_to": "cand-1",
            "related_to_type": "candidate",
            "folder": "Resumes",
        }
        # httpx multipart text-part shape: (filename=None, content=url_string)
        assert captured["files"] == {"files[]": (None, "https://example.com/resume.pdf")}
        assert result["file_link"] == "https://cdn/x.pdf"

    @pytest.mark.anyio
    async def test_returns_empty_dict_when_post_multipart_returns_none(self, monkeypatch):
        async def mock_post_multipart(path, form, files, params=None):
            return None

        monkeypatch.setattr(client, "post_multipart", mock_post_multipart)
        result = await client.upload_file(
            file_url="https://x.com/f.pdf",
            related_to="cand-1",
            related_to_type="candidate",
            folder="Uploads",
        )
        assert result == {}
