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
    async def test_title_filter(self, monkeypatch):
        async def mock_get(path, params=None):
            assert path == "/meetings/search"
            assert params["title"] == "Interview"
            return {"data": [{"title": "Interview"}]}

        monkeypatch.setattr(client, "get", mock_get)
        results = await client.search_meetings(title="Interview")
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
        mock_client.get = AsyncMock(side_effect=[rate_limited, success])
        monkeypatch.setattr(client, "_client", mock_client)

        with patch("recruit_crm_mcp.client.anyio.sleep") as mock_sleep:
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

        with patch("recruit_crm_mcp.client.anyio.sleep"):
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

        with patch("recruit_crm_mcp.client.anyio.sleep"):
            with caplog.at_level(logging.WARNING, logger="recruit_crm_mcp.client"):
                await client.get("/candidates")

        assert "Rate limited" in caplog.text
        assert "/candidates" in caplog.text
