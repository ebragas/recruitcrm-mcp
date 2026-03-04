import pytest

from recruit_crm_mcp.server import (
    ping,
    __version__,
    get_assigned_candidates,
    get_company,
    get_contact,
    get_meeting,
    get_note,
    get_task,
    search_companies,
    search_contacts,
    search_meetings,
    search_notes,
    search_tasks,
)


def test_ping_returns_ok():
    result = ping()
    assert result["status"] == "ok"
    assert result["version"] == __version__


def test_ping_reports_no_api_key(monkeypatch):
    monkeypatch.delenv("RECRUIT_CRM_API_KEY", raising=False)
    result = ping()
    assert result["api_configured"] is False


def test_ping_reports_api_key_configured(monkeypatch):
    monkeypatch.setenv("RECRUIT_CRM_API_KEY", "test-key")
    result = ping()
    assert result["api_configured"] is True


class TestGetContactTool:
    @pytest.mark.anyio
    async def test_returns_full_record(self, monkeypatch):
        """get_contact should return the full raw contact record."""
        raw_contact = {
            "slug": "contact-123",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
        }

        async def mock_get_contact(slug):
            assert slug == "contact-123"
            return raw_contact

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "get_contact", mock_get_contact)

        result = await get_contact("contact-123")
        assert result == raw_contact


class TestSearchContactsTool:
    @pytest.mark.anyio
    async def test_returns_summarized_list(self, monkeypatch):
        """Without contact_slug, should return summarized contact list."""
        mock_data = [
            {
                "slug": "contact-123",
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane@example.com",
                "contact_number": "+1234567890",
                "designation": "VP Sales",
                "company_slug": "acme-corp",
                "city": "Austin",
                "state": "Texas",
                "country": "US",
                "linkedin": None,
            },
        ]

        async def mock_search(**kwargs):
            return mock_data

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "search_contacts", mock_search)

        results = await search_contacts(email="jane@example.com")
        assert len(results) == 1
        assert results[0].slug == "contact-123"
        assert results[0].name == "Jane Doe"
        assert results[0].designation == "VP Sales"


class TestGetNoteTool:
    @pytest.mark.anyio
    async def test_returns_full_record(self, monkeypatch):
        """get_note should return the full raw note record."""
        raw_note = {
            "id": 12345,
            "note_type": {"id": 1, "label": "Note"},
            "description": "A note",
        }

        async def mock_get_note(note_id):
            assert note_id == 12345
            return raw_note

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "get_note", mock_get_note)

        result = await get_note(12345)
        assert result == raw_note


class TestSearchNotesTool:
    @pytest.mark.anyio
    async def test_returns_summarized_list(self, monkeypatch):
        """Filtered search should return summarized note list."""
        mock_data = [
            {
                "id": 12345,
                "note_type": {"id": 1, "label": "Note"},
                "description": "Follow up note",
                "related_to": "cand-123",
                "related_to_type": "candidate",
                "created_on": "2025-04-29T17:39:50.000000Z",
                "updated_on": "2025-04-29T17:55:30.000000Z",
            },
        ]

        async def mock_search(**kwargs):
            return mock_data

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "search_notes", mock_search)

        results = await search_notes(created_from="2025-01-01")
        assert len(results) == 1
        assert results[0].id == 12345
        assert results[0].note_type == "Note"

    @pytest.mark.anyio
    async def test_maps_created_from_to_added_from(self, monkeypatch):
        """The tool should map created_from/to to added_from/to internally."""
        captured = {}

        async def mock_search(**kwargs):
            captured.update(kwargs)
            return []

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "search_notes", mock_search)

        await search_notes(created_from="2025-01-01", created_to="2025-06-30")
        assert captured["added_from"] == "2025-01-01"
        assert captured["added_to"] == "2025-06-30"


class TestGetTaskTool:
    @pytest.mark.anyio
    async def test_returns_full_record(self, monkeypatch):
        """get_task should return the full raw task record."""
        raw_task = {
            "id": 12345,
            "title": "Follow up",
            "task_type": None,
            "status": 0,
        }

        async def mock_get_task(task_id):
            assert task_id == 12345
            return raw_task

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "get_task", mock_get_task)

        result = await get_task(12345)
        assert result == raw_task


class TestSearchTasksTool:
    @pytest.mark.anyio
    async def test_returns_summarized_list(self, monkeypatch):
        """Filtered search should return summarized task list."""
        mock_data = [
            {
                "id": 12345,
                "title": "Follow up",
                "task_type": {"id": 1, "label": "Call"},
                "status": 0,
                "start_date": "2025-04-29T18:30:00.000000Z",
                "related_to": "cand-123",
                "related_to_type": "candidate",
                "related_to_name": "Jane Doe",
                "owner": 31585,
                "reminder_date": None,
            },
        ]

        async def mock_search(**kwargs):
            return mock_data

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "search_tasks", mock_search)

        results = await search_tasks(title="Follow up")
        assert len(results) == 1
        assert results[0].id == 12345
        assert results[0].title == "Follow up"
        assert results[0].task_type == "Call"


class TestGetCompanyTool:
    @pytest.mark.anyio
    async def test_returns_full_record(self, monkeypatch):
        """get_company should return the full raw company record."""
        raw_company = {
            "slug": "acme-corp",
            "company_name": "Acme Corp",
            "website": "https://acme.com",
        }

        async def mock_get_company(slug):
            assert slug == "acme-corp"
            return raw_company

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "get_company", mock_get_company)

        result = await get_company("acme-corp")
        assert result == raw_company


class TestSearchCompaniesTool:
    @pytest.mark.anyio
    async def test_returns_summarized_list(self, monkeypatch):
        """Filtered search should return summarized company list."""
        mock_data = [
            {
                "slug": "acme-corp",
                "company_name": "Acme Corp",
                "about_company": "A great company",
                "website": "https://acme.com",
                "city": "Austin",
                "state": "Texas",
                "country": "US",
                "linkedin": None,
                "industry_id": 42,
                "is_parent_company": 0,
                "is_child_company": 0,
            },
        ]

        async def mock_search(**kwargs):
            return mock_data

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "search_companies", mock_search)

        results = await search_companies(company_name="Acme")
        assert len(results) == 1
        assert results[0].slug == "acme-corp"
        assert results[0].company_name == "Acme Corp"


class TestGetMeetingTool:
    @pytest.mark.anyio
    async def test_returns_full_record(self, monkeypatch):
        """get_meeting should return the full raw meeting record."""
        raw_meeting = {
            "id": 12345,
            "title": "Interview",
            "meeting_type": {"id": 1, "label": "Interview"},
            "status": 0,
        }

        async def mock_get_meeting(meeting_id):
            assert meeting_id == 12345
            return raw_meeting

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "get_meeting", mock_get_meeting)

        result = await get_meeting(12345)
        assert result == raw_meeting


class TestSearchMeetingsTool:
    @pytest.mark.anyio
    async def test_returns_summarized_list(self, monkeypatch):
        """Without meeting_id, should return summarized meeting list."""
        mock_data = [
            {
                "id": 12345,
                "title": "Interview",
                "meeting_type": {"id": 1, "label": "Phone Screen"},
                "status": 0,
                "start_date": "2025-04-29T18:30:00.000000Z",
                "end_date": "2025-04-29T19:00:00.000000Z",
                "all_day": 0,
                "address": "Zoom",
                "related_to": "cand-123",
                "related_to_type": "candidate",
                "owner": 31585,
            },
        ]

        async def mock_search(**kwargs):
            return mock_data

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "search_meetings", mock_search)

        results = await search_meetings(title="Interview")
        assert len(results) == 1
        assert results[0].id == 12345
        assert results[0].title == "Interview"
        assert results[0].meeting_type == "Phone Screen"


class TestGetAssignedCandidates:
    """Test that the get_assigned_candidates tool produces correct summaries."""

    @pytest.mark.anyio
    async def test_summarizes_candidate_with_hiring_status(self, monkeypatch):
        """Tool should return candidate summary fields + hiring_status."""
        mock_data = [
            {
                "candidate": {
                    "slug": "cand-123",
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "email": "jane@example.com",
                    "position": "Engineer",
                    "current_organization": "Acme",
                    "city": "Austin",
                },
                "status": {"id": 5, "label": "Interview"},
            },
        ]

        async def mock_get_assigned(job_slug, status_id=None, limit=25):
            return mock_data

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "get_assigned_candidates", mock_get_assigned)

        results = await get_assigned_candidates("job-123")
        assert len(results) == 1
        summary = results[0]
        assert summary.slug == "cand-123"
        assert summary.name == "Jane Doe"
        assert summary.email == "jane@example.com"
        assert summary.position == "Engineer"
        assert summary.company == "Acme"
        assert summary.city == "Austin"
        assert summary.hiring_status == "Interview"

    @pytest.mark.anyio
    async def test_missing_status_gives_none(self, monkeypatch):
        """When status is missing, hiring_status should be None."""
        mock_data = [
            {
                "candidate": {"slug": "cand-456", "first_name": "John", "last_name": "Smith"},
            },
        ]

        async def mock_get_assigned(job_slug, status_id=None, limit=25):
            return mock_data

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "get_assigned_candidates", mock_get_assigned)

        results = await get_assigned_candidates("job-123")
        assert len(results) == 1
        assert results[0].slug == "cand-456"
        assert results[0].hiring_status is None
