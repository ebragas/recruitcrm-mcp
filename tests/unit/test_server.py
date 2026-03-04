import pytest

from recruit_crm_mcp.server import (
    ping,
    __version__,
    _summarize_candidate,
    _summarize_company,
    _summarize_contact,
    _summarize_job,
    _summarize_meeting,
    _summarize_task,
    _summarize_user,
    _job_location_label,
    get_assigned_candidates,
    search_companies,
    search_contacts,
    search_meetings,
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


class TestSummarizeContact:
    def test_basic_fields(self):
        raw = {
            "slug": "contact-123",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "contact_number": "+1234567890",
            "designation": "VP Sales",
            "company_slug": "acme-corp",
            "city": "Austin",
            "state": "Texas",
            "country": "United States",
            "linkedin": "https://linkedin.com/in/janedoe",
        }
        result = _summarize_contact(raw)
        assert result["slug"] == "contact-123"
        assert result["name"] == "Jane Doe"
        assert result["email"] == "jane@example.com"
        assert result["contact_number"] == "+1234567890"
        assert result["designation"] == "VP Sales"
        assert result["company_slug"] == "acme-corp"
        assert result["city"] == "Austin"
        assert result["state"] == "Texas"
        assert result["country"] == "United States"
        assert result["linkedin"] == "https://linkedin.com/in/janedoe"

    def test_empty_record(self):
        result = _summarize_contact({})
        assert result["slug"] is None
        assert result["name"] == ""
        assert result["email"] is None
        assert result["contact_number"] is None
        assert result["designation"] is None
        assert result["company_slug"] is None
        assert result["city"] is None
        assert result["state"] is None
        assert result["country"] is None
        assert result["linkedin"] is None


class TestSearchContactsTool:
    @pytest.mark.anyio
    async def test_contact_slug_short_circuits_to_get(self, monkeypatch):
        """When contact_slug is provided, should call get_contact directly."""
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

        result = await search_contacts(contact_slug="contact-123")
        assert result == raw_contact

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
        assert results[0]["slug"] == "contact-123"
        assert results[0]["name"] == "Jane Doe"
        assert results[0]["designation"] == "VP Sales"


class TestSummarizeTask:
    def test_basic_fields(self):
        raw = {
            "id": 44261638,
            "title": "Follow up with Jane",
            "task_type": {"id": 1, "label": "Call"},
            "status": 0,
            "start_date": "2025-04-29T18:30:00.000000Z",
            "related_to": "cand-slug-123",
            "related_to_type": "candidate",
            "related_to_name": "Jane Doe",
            "owner": 31585,
            "reminder_date": "2025-04-29T18:00:00.000000Z",
        }
        result = _summarize_task(raw)
        assert result["id"] == 44261638
        assert result["title"] == "Follow up with Jane"
        assert result["task_type"] == "Call"
        assert result["status"] == 0
        assert result["start_date"] == "2025-04-29T18:30:00.000000Z"
        assert result["related_to"] == "cand-slug-123"
        assert result["related_to_type"] == "candidate"
        assert result["related_to_name"] == "Jane Doe"
        assert result["owner"] == 31585
        assert result["reminder_date"] == "2025-04-29T18:00:00.000000Z"

    def test_empty_record(self):
        result = _summarize_task({})
        assert result["id"] is None
        assert result["title"] is None
        assert result["task_type"] is None
        assert result["status"] is None
        assert result["start_date"] is None
        assert result["related_to"] is None
        assert result["related_to_type"] is None
        assert result["related_to_name"] is None
        assert result["owner"] is None
        assert result["reminder_date"] is None

    def test_null_task_type(self):
        result = _summarize_task({"task_type": None})
        assert result["task_type"] is None


class TestSearchTasksTool:
    @pytest.mark.anyio
    async def test_task_id_short_circuits_to_get(self, monkeypatch):
        """When task_id is provided, should call get_task directly."""
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

        result = await search_tasks(task_id=12345)
        assert result == raw_task

    @pytest.mark.anyio
    async def test_returns_summarized_list(self, monkeypatch):
        """Without task_id, should return summarized task list."""
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
        assert results[0]["id"] == 12345
        assert results[0]["title"] == "Follow up"
        assert results[0]["task_type"] == "Call"


class TestSummarizeCompany:
    def test_basic_fields(self):
        raw = {
            "slug": "acme-corp",
            "company_name": "Acme Corp",
            "about_company": "A great company",
            "website": "https://acme.com",
            "city": "Austin",
            "state": "Texas",
            "country": "United States",
            "linkedin": "https://linkedin.com/company/acme",
            "industry_id": 42,
            "is_parent_company": 1,
            "is_child_company": 0,
        }
        result = _summarize_company(raw)
        assert result["slug"] == "acme-corp"
        assert result["company_name"] == "Acme Corp"
        assert result["about_company"] == "A great company"
        assert result["website"] == "https://acme.com"
        assert result["city"] == "Austin"
        assert result["state"] == "Texas"
        assert result["country"] == "United States"
        assert result["linkedin"] == "https://linkedin.com/company/acme"
        assert result["industry_id"] == 42
        assert result["is_parent_company"] == 1
        assert result["is_child_company"] == 0

    def test_empty_record(self):
        result = _summarize_company({})
        assert result["slug"] is None
        assert result["company_name"] is None
        assert result["about_company"] is None
        assert result["website"] is None
        assert result["city"] is None
        assert result["state"] is None
        assert result["country"] is None
        assert result["linkedin"] is None
        assert result["industry_id"] is None
        assert result["is_parent_company"] is None
        assert result["is_child_company"] is None


class TestSearchCompaniesTool:
    @pytest.mark.anyio
    async def test_company_slug_short_circuits_to_get(self, monkeypatch):
        """When company_slug is provided, should call get_company directly."""
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

        result = await search_companies(company_slug="acme-corp")
        assert result == raw_company

    @pytest.mark.anyio
    async def test_returns_summarized_list(self, monkeypatch):
        """Without company_slug, should return summarized company list."""
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
        assert results[0]["slug"] == "acme-corp"
        assert results[0]["company_name"] == "Acme Corp"


class TestSummarizeMeeting:
    def test_basic_fields(self):
        raw = {
            "id": 37639022,
            "title": "Interview with Jane",
            "meeting_type": {"id": 40014, "label": "Candidate Interview"},
            "status": 0,
            "start_date": "2025-04-29T18:30:00.000000Z",
            "end_date": "2025-04-29T19:00:00.000000Z",
            "all_day": 0,
            "address": "123 Main St",
            "related_to": "cand-slug-123",
            "related_to_type": "candidate",
            "owner": 31585,
        }
        result = _summarize_meeting(raw)
        assert result["id"] == 37639022
        assert result["title"] == "Interview with Jane"
        assert result["meeting_type"] == "Candidate Interview"
        assert result["status"] == 0
        assert result["start_date"] == "2025-04-29T18:30:00.000000Z"
        assert result["end_date"] == "2025-04-29T19:00:00.000000Z"
        assert result["all_day"] == 0
        assert result["address"] == "123 Main St"
        assert result["related_to"] == "cand-slug-123"
        assert result["related_to_type"] == "candidate"
        assert result["owner"] == 31585

    def test_empty_record(self):
        result = _summarize_meeting({})
        assert result["id"] is None
        assert result["title"] is None
        assert result["meeting_type"] is None
        assert result["status"] is None
        assert result["start_date"] is None
        assert result["end_date"] is None
        assert result["all_day"] is None
        assert result["address"] is None
        assert result["related_to"] is None
        assert result["related_to_type"] is None
        assert result["owner"] is None


class TestSearchMeetingsTool:
    @pytest.mark.anyio
    async def test_meeting_id_short_circuits_to_get(self, monkeypatch):
        """When meeting_id is provided, should call get_meeting directly."""
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

        result = await search_meetings(meeting_id=12345)
        assert result == raw_meeting

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
        assert results[0]["id"] == 12345
        assert results[0]["title"] == "Interview"
        assert results[0]["meeting_type"] == "Phone Screen"


class TestSummarizeCandidate:
    def test_basic_fields(self):
        raw = {
            "slug": "17720468790770031585gzy",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "position": "Engineer",
            "current_organization": "Acme",
            "city": "Austin",
        }
        result = _summarize_candidate(raw)
        assert result["slug"] == "17720468790770031585gzy"
        assert result["name"] == "Jane Doe"
        assert result["email"] == "jane@example.com"
        assert result["position"] == "Engineer"
        assert result["company"] == "Acme"
        assert result["city"] == "Austin"

    def test_empty_record(self):
        result = _summarize_candidate({})
        assert result["slug"] is None
        assert result["name"] == ""
        assert result["email"] is None
        assert result["position"] is None
        assert result["company"] is None
        assert result["city"] is None


class TestSummarizeJob:
    def test_basic_fields(self):
        raw = {
            "slug": "17648707064020043135awk",
            "name": "Backend Engineer",
            "job_status": {"id": 1, "label": "Open"},
            "city": "Austin",
            "country": "US",
            "job_type": "Full-time",
            "job_location_type": "1",
            "minimum_experience": "2",
            "maximum_experience": "5",
            "min_annual_salary": "80000",
            "max_annual_salary": "120000",
            "pay_rate": "0",
            "bill_rate": "0",
            "job_category": "Engineering",
            "note_for_candidates": "Great team!",
            "job_description_file": None,
        }
        result = _summarize_job(raw)
        assert result["slug"] == "17648707064020043135awk"
        assert result["name"] == "Backend Engineer"
        assert result["status"] == "Open"
        assert result["city"] == "Austin"
        assert result["country"] == "US"
        assert result["job_type"] == "Full-time"
        assert result["job_location_type"] == "Remote"
        assert result["minimum_experience"] == "2"
        assert result["maximum_experience"] == "5"
        assert result["min_annual_salary"] == "80000"
        assert result["max_annual_salary"] == "120000"
        assert result["pay_rate"] == "0"
        assert result["bill_rate"] == "0"
        assert result["job_category"] == "Engineering"
        assert result["note_for_candidates"] == "Great team!"
        assert result["job_description_file"] is None

    def test_no_status(self):
        raw = {"slug": "abc", "name": "Designer"}
        result = _summarize_job(raw)
        assert result["slug"] == "abc"
        assert result["name"] == "Designer"
        assert result["status"] is None
        assert result["city"] is None
        assert result["country"] is None
        assert result["job_location_type"] == ""


class TestJobLocationLabel:
    def test_remote(self):
        assert _job_location_label("1") == "Remote"

    def test_hybrid(self):
        assert _job_location_label("2") == "Hybrid"

    def test_onsite(self):
        assert _job_location_label("0") == "On-site"

    def test_unknown_value(self):
        assert _job_location_label("99") == "99"

    def test_none(self):
        assert _job_location_label(None) == ""


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
        assert summary["slug"] == "cand-123"
        assert summary["name"] == "Jane Doe"
        assert summary["email"] == "jane@example.com"
        assert summary["position"] == "Engineer"
        assert summary["company"] == "Acme"
        assert summary["city"] == "Austin"
        assert summary["hiring_status"] == "Interview"

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
        assert results[0]["slug"] == "cand-456"
        assert results[0]["hiring_status"] is None


class TestSummarizeUser:
    def test_basic_fields(self):
        raw = {
            "id": 43135,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "role": "Admin",
        }
        result = _summarize_user(raw)
        assert result["id"] == 43135
        assert result["name"] == "Jane Doe"
        assert result["email"] == "jane@example.com"
        assert result["role"] == "Admin"

    def test_empty_record(self):
        result = _summarize_user({})
        assert result["id"] is None
        assert result["name"] == ""
        assert result["email"] is None
        assert result["role"] is None
