import pytest
from fastmcp.exceptions import ToolError

from recruit_crm_mcp.client import RecruitCrmError
from recruit_crm_mcp.models import (
    Associations,
    CustomFieldValue,
    EntityRef,
    LookupItem,
    WriteResult,
)
from recruit_crm_mcp.server import (
    ping,
    __version__,
    assign_candidate,
    create_candidate,
    create_company,
    create_contact,
    create_job,
    create_note,
    create_task,
    delete_note,
    get_assigned_candidates,
    get_company,
    get_contact,
    get_meeting,
    get_note,
    get_task,
    list_candidate_custom_fields,
    list_company_custom_fields,
    list_contact_custom_fields,
    list_contact_stages,
    list_hiring_pipeline_stages,
    list_hiring_pipelines,
    list_industries,
    list_job_custom_fields,
    list_meeting_types,
    list_note_types,
    list_task_types,
    log_meeting,
    search_companies,
    search_contacts,
    search_meetings,
    search_notes,
    search_tasks,
    set_candidate_custom_fields,
    set_company_custom_fields,
    set_contact_custom_fields,
    set_job_custom_fields,
    unassign_candidate,
    update_candidate,
    update_company,
    update_contact,
    update_hiring_stage,
    update_job,
    update_meeting,
    update_task,
    upload_file,
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


class TestWriteResultTitleFallback:
    """The title fallback chain is the only shared piece of ``_write_result_from`` —
    pin each branch so future tweaks don't silently regress."""

    def test_prefers_title(self):
        from recruit_crm_mcp.server import _write_result_from

        result = _write_result_from("note", {"id": 1, "title": "T", "name": "N"})
        assert result.title == "T"

    def test_falls_back_to_name(self):
        from recruit_crm_mcp.server import _write_result_from

        result = _write_result_from("job", {"slug": "j", "name": "Senior Eng"})
        assert result.title == "Senior Eng"

    def test_falls_back_to_company_name(self):
        from recruit_crm_mcp.server import _write_result_from

        result = _write_result_from("company", {"slug": "acme", "company_name": "Acme"})
        assert result.title == "Acme"

    def test_falls_back_to_person_name(self):
        from recruit_crm_mcp.server import _write_result_from

        result = _write_result_from(
            "candidate",
            {"slug": "c1", "first_name": "Jane", "last_name": "Doe"},
        )
        assert result.title == "Jane Doe"

    def test_person_name_handles_missing_last_name(self):
        from recruit_crm_mcp.server import _write_result_from

        result = _write_result_from("contact", {"slug": "c1", "first_name": "Jane"})
        assert result.title == "Jane"

    def test_returns_none_when_no_title_field_present(self):
        from recruit_crm_mcp.server import _write_result_from

        result = _write_result_from("contact", {"slug": "c1"})
        assert result.title is None


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


class TestListNoteTypesTool:
    @pytest.mark.anyio
    async def test_returns_lookup_items(self, monkeypatch):
        async def mock_list():
            return [{"id": 1, "label": "Note"}, {"id": 2, "label": "Call"}]

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "list_note_types", mock_list)

        results = await list_note_types()
        assert len(results) == 2
        assert all(isinstance(item, LookupItem) for item in results)
        assert results[0].id == 1
        assert results[0].label == "Note"


class TestListMeetingTypesTool:
    @pytest.mark.anyio
    async def test_returns_lookup_items(self, monkeypatch):
        async def mock_list():
            return [{"id": 1, "label": "Client Meeting"}]

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "list_meeting_types", mock_list)

        results = await list_meeting_types()
        assert len(results) == 1
        assert isinstance(results[0], LookupItem)
        assert results[0].label == "Client Meeting"


class TestListTaskTypesTool:
    @pytest.mark.anyio
    async def test_returns_lookup_items(self, monkeypatch):
        async def mock_list():
            return [{"id": 1, "label": "Follow up"}]

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "list_task_types", mock_list)

        results = await list_task_types()
        assert len(results) == 1
        assert isinstance(results[0], LookupItem)
        assert results[0].label == "Follow up"


class TestListHiringPipelinesTool:
    @pytest.mark.anyio
    async def test_returns_lookup_items(self, monkeypatch):
        async def mock_list():
            return [{"id": 0, "label": "Master Hiring Pipeline"}]

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "list_hiring_pipelines", mock_list)

        results = await list_hiring_pipelines()
        assert len(results) == 1
        assert isinstance(results[0], LookupItem)
        assert results[0].id == 0
        assert results[0].label == "Master Hiring Pipeline"


class TestListHiringPipelineStagesTool:
    @pytest.mark.anyio
    async def test_passes_pipeline_id_through(self, monkeypatch):
        captured = {}

        async def mock_list(pipeline_id):
            captured["pipeline_id"] = pipeline_id
            return [{"id": 56, "label": "Lead"}]

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "list_hiring_pipeline_stages", mock_list)

        results = await list_hiring_pipeline_stages(7)
        assert captured["pipeline_id"] == 7
        assert len(results) == 1
        assert isinstance(results[0], LookupItem)
        assert results[0].id == 56


class TestListContactStagesTool:
    @pytest.mark.anyio
    async def test_returns_lookup_items(self, monkeypatch):
        async def mock_list():
            return [{"id": 56, "label": "Lead"}]

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "list_contact_stages", mock_list)

        results = await list_contact_stages()
        assert len(results) == 1
        assert isinstance(results[0], LookupItem)
        assert results[0].label == "Lead"


class TestListIndustriesTool:
    @pytest.mark.anyio
    async def test_returns_lookup_items(self, monkeypatch):
        async def mock_list():
            return [{"id": 6, "label": "Apparel and Fashion"}]

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "list_industries", mock_list)

        results = await list_industries()
        assert len(results) == 1
        assert isinstance(results[0], LookupItem)
        assert results[0].id == 6


class TestListCompanyCustomFieldsTool:
    @pytest.mark.anyio
    async def test_returns_lookup_items(self, monkeypatch):
        async def mock_list():
            return [
                {
                    "id": 1,
                    "label": "Revenue",
                    "field_id": 1,
                    "field_name": "Revenue",
                    "field_type": "text",
                },
            ]

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "list_company_custom_fields", mock_list)

        results = await list_company_custom_fields()
        assert len(results) == 1
        assert isinstance(results[0], LookupItem)
        assert results[0].id == 1
        assert results[0].label == "Revenue"


class TestListContactCustomFieldsTool:
    @pytest.mark.anyio
    async def test_returns_lookup_items(self, monkeypatch):
        async def mock_list():
            return [{"id": 2, "label": "Hobbies", "field_type": "text"}]

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "list_contact_custom_fields", mock_list)

        results = await list_contact_custom_fields()
        assert len(results) == 1
        assert isinstance(results[0], LookupItem)
        assert results[0].label == "Hobbies"


class TestListJobCustomFieldsTool:
    @pytest.mark.anyio
    async def test_returns_lookup_items(self, monkeypatch):
        async def mock_list():
            return [{"id": 3, "label": "Priority", "field_type": "select"}]

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "list_job_custom_fields", mock_list)

        results = await list_job_custom_fields()
        assert len(results) == 1
        assert isinstance(results[0], LookupItem)
        assert results[0].label == "Priority"


class TestListCandidateCustomFieldsTool:
    @pytest.mark.anyio
    async def test_returns_lookup_items(self, monkeypatch):
        async def mock_list():
            return [{"id": 4, "label": "GitHub", "field_type": "url"}]

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "list_candidate_custom_fields", mock_list)

        results = await list_candidate_custom_fields()
        assert len(results) == 1
        assert isinstance(results[0], LookupItem)
        assert results[0].label == "GitHub"


class TestLogMeetingTool:
    @pytest.mark.anyio
    async def test_flattens_entity_ref_and_joins_attendees(self, monkeypatch):
        captured: dict = {}

        async def mock_create_meeting(payload):
            captured["payload"] = payload
            return {"id": 42, "title": "Intro Call"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_meeting", mock_create_meeting)

        result = await log_meeting(
            title="Intro Call",
            start_date="2025-04-29T18:30:00Z",
            end_date="2025-04-29T19:00:00Z",
            related_to=EntityRef(kind="candidate", id="cand-1"),
            attendee_contacts=["con-1", "con-2"],
            attendee_candidates=["cand-1"],
            attendee_users=[29998, 23453],
            associated=Associations(companies=["co-1"], jobs=["job-1"]),
        )

        payload = captured["payload"]
        assert payload["related_to"] == "cand-1"
        assert payload["related_to_type"] == "candidate"
        assert payload["attendee_contacts"] == "con-1,con-2"
        assert payload["attendee_candidates"] == "cand-1"
        assert payload["attendee_users"] == "29998,23453"
        assert payload["associated_companies"] == "co-1"
        assert payload["associated_jobs"] == "job-1"
        # Empty associations should not appear at all
        assert "associated_candidates" not in payload
        assert "associated_contacts" not in payload
        assert "associated_deals" not in payload
        # Defaults flow through — bool serialized to "1"/"0" (API rejects JSON false)
        assert payload["do_not_send_calendar_invites"] == "1"
        assert payload["reminder"] == -1
        # Result
        assert isinstance(result, WriteResult)
        assert result.kind == "meeting"
        assert result.id == "42"
        assert result.title == "Intro Call"

    @pytest.mark.anyio
    async def test_omits_empty_lists_and_nones(self, monkeypatch):
        captured: dict = {}

        async def mock_create_meeting(payload):
            captured["payload"] = payload
            return {"id": 1}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_meeting", mock_create_meeting)

        await log_meeting(
            title="t",
            start_date="2025-01-01T00:00:00Z",
            end_date="2025-01-01T01:00:00Z",
            related_to=EntityRef(kind="company", id="co-1"),
        )

        payload = captured["payload"]
        for k in (
            "attendee_contacts",
            "attendee_candidates",
            "attendee_users",
            "associated_candidates",
            "associated_companies",
            "associated_contacts",
            "associated_jobs",
            "associated_deals",
            "description",
            "address",
            "meeting_type_id",
            "owner_id",
        ):
            assert k not in payload, f"expected {k!r} absent, got {payload[k]!r}"

    @pytest.mark.anyio
    async def test_do_not_send_false_serializes_to_string_zero(self, monkeypatch):
        """Python ``False`` must become string ``"0"`` — the live API rejects
        JSON ``false`` with 422, accepts ``"0"``.
        """
        captured: dict = {}

        async def mock_create_meeting(payload):
            captured["payload"] = payload
            return {"id": 1}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_meeting", mock_create_meeting)

        await log_meeting(
            title="t",
            start_date="2025-01-01T00:00:00Z",
            end_date="2025-01-01T01:00:00Z",
            related_to=EntityRef(kind="candidate", id="cand-1"),
            do_not_send_calendar_invites=False,
        )

        assert captured["payload"]["do_not_send_calendar_invites"] == "0"


class TestCreateNoteTool:
    @pytest.mark.anyio
    async def test_flattens_and_returns_write_result(self, monkeypatch):
        captured: dict = {}

        async def mock_create_note(payload):
            captured["payload"] = payload
            return {"id": 7}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_note", mock_create_note)

        result = await create_note(
            description="Spoke with candidate",
            related_to=EntityRef(kind="candidate", id="cand-1"),
            note_type_id=3,
            associated=Associations(companies=["co-1", "co-2"], jobs=["job-1"]),
        )

        payload = captured["payload"]
        assert payload["description"] == "Spoke with candidate"
        assert payload["related_to"] == "cand-1"
        assert payload["related_to_type"] == "candidate"
        assert payload["note_type_id"] == 3
        assert payload["associated_companies"] == "co-1,co-2"
        assert payload["associated_jobs"] == "job-1"
        assert "associated_candidates" not in payload
        assert "associated_contacts" not in payload
        assert "associated_deals" not in payload
        assert isinstance(result, WriteResult)
        assert result.kind == "note"
        assert result.id == "7"

    @pytest.mark.anyio
    async def test_omits_empty_associations_and_none_note_type(self, monkeypatch):
        captured: dict = {}

        async def mock_create_note(payload):
            captured["payload"] = payload
            return {"id": 1}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_note", mock_create_note)

        await create_note(
            description="x",
            related_to=EntityRef(kind="job", id="job-1"),
        )

        payload = captured["payload"]
        assert "note_type_id" not in payload
        for k in (
            "associated_candidates",
            "associated_companies",
            "associated_contacts",
            "associated_jobs",
            "associated_deals",
        ):
            assert k not in payload


class TestCreateTaskTool:
    @pytest.mark.anyio
    async def test_defaults_reminder_to_1440(self, monkeypatch):
        captured: dict = {}

        async def mock_create_task(payload):
            captured["payload"] = payload
            return {"id": 9, "title": "Follow up"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_task", mock_create_task)

        result = await create_task(
            title="Follow up",
            start_date="2025-05-01T09:00:00Z",
        )

        payload = captured["payload"]
        assert payload["title"] == "Follow up"
        assert payload["start_date"] == "2025-05-01T09:00:00Z"
        assert payload["reminder"] == 1440
        # No related_to when omitted
        assert "related_to" not in payload
        assert "related_to_type" not in payload
        assert isinstance(result, WriteResult)
        assert result.kind == "task"
        assert result.id == "9"
        assert result.title == "Follow up"

    @pytest.mark.anyio
    async def test_related_to_flattened_when_provided(self, monkeypatch):
        captured: dict = {}

        async def mock_create_task(payload):
            captured["payload"] = payload
            return {"id": 1}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_task", mock_create_task)

        await create_task(
            title="Call",
            start_date="2025-05-01T09:00:00Z",
            related_to=EntityRef(kind="contact", id="con-1"),
            associated=Associations(jobs=["job-1"]),
        )

        payload = captured["payload"]
        assert payload["related_to"] == "con-1"
        assert payload["related_to_type"] == "contact"
        assert payload["associated_jobs"] == "job-1"
        assert "associated_candidates" not in payload


class TestUpdateTaskTool:
    @pytest.mark.anyio
    async def test_forwards_only_non_none_patch(self, monkeypatch):
        captured: dict = {}

        async def mock_update_task(task_id, patch):
            captured["task_id"] = task_id
            captured["patch"] = patch
            return {"id": task_id, "title": "x", "status": patch.get("status")}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_task", mock_update_task)

        result = await update_task(task_id=42, status="c")

        assert captured["task_id"] == 42
        assert captured["patch"] == {"status": "c"}
        assert isinstance(result, WriteResult)
        assert result.kind == "task"
        assert result.id == "42"

    @pytest.mark.anyio
    async def test_forwards_multiple_fields(self, monkeypatch):
        captured: dict = {}

        async def mock_update_task(task_id, patch):
            captured["task_id"] = task_id
            captured["patch"] = patch
            return {"id": task_id}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_task", mock_update_task)

        await update_task(
            task_id=5,
            title="New title",
            start_date="2025-06-01T00:00:00Z",
            description="d",
            status="o",
            owner_id=1234,
        )

        assert captured["task_id"] == 5
        assert captured["patch"] == {
            "title": "New title",
            "start_date": "2025-06-01T00:00:00Z",
            "description": "d",
            "status": "o",
            "owner_id": 1234,
        }

    @pytest.mark.anyio
    async def test_forwards_task_type_id_to_client(self, monkeypatch):
        captured: dict = {}

        async def mock_update_task(task_id, patch):
            captured["task_id"] = task_id
            captured["patch"] = patch
            return {"id": task_id}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_task", mock_update_task)

        await update_task(task_id=99, task_type_id=3)

        assert captured["task_id"] == 99
        assert captured["patch"] == {"task_type_id": 3}


# ---------------------------------------------------------------------------
# Company write tools
# ---------------------------------------------------------------------------


class TestCreateCompanyTool:
    @pytest.mark.anyio
    async def test_builds_payload_and_returns_write_result(self, monkeypatch):
        captured: dict = {}

        async def mock_create_company(payload):
            captured["payload"] = payload
            return {"slug": "acme", "company_name": "Acme"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_company", mock_create_company)

        result = await create_company(
            company_name="Acme",
            city="NYC",
            industry_id=7,
            custom_fields=[CustomFieldValue(field_id=1, value="Enterprise")],
        )

        payload = captured["payload"]
        assert payload["company_name"] == "Acme"
        assert payload["city"] == "NYC"
        assert payload["industry_id"] == 7
        assert payload["custom_fields"] == [{"field_id": 1, "value": "Enterprise"}]
        # None-stripped
        assert "about_company" not in payload
        assert "website" not in payload
        assert "owner_id" not in payload
        assert isinstance(result, WriteResult)
        assert result.kind == "company"
        assert result.id == "acme"
        assert result.title == "Acme"

    @pytest.mark.anyio
    async def test_omits_custom_fields_when_empty(self, monkeypatch):
        captured: dict = {}

        async def mock_create_company(payload):
            captured["payload"] = payload
            return {"slug": "acme"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_company", mock_create_company)

        await create_company(company_name="Acme")

        assert "custom_fields" not in captured["payload"]


class TestUpdateCompanyTool:
    @pytest.mark.anyio
    async def test_forwards_only_non_none_patch(self, monkeypatch):
        captured: dict = {}

        async def mock_update_company(slug, patch):
            captured["slug"] = slug
            captured["patch"] = patch
            return {"slug": slug, "company_name": "Acme"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_company", mock_update_company)

        result = await update_company(slug="acme", city="Boston")

        assert captured["slug"] == "acme"
        assert captured["patch"] == {"city": "Boston"}
        assert isinstance(result, WriteResult)
        assert result.kind == "company"
        assert result.id == "acme"

    @pytest.mark.anyio
    async def test_custom_fields_serialized(self, monkeypatch):
        captured: dict = {}

        async def mock_update_company(slug, patch):
            captured["slug"] = slug
            captured["patch"] = patch
            return {"slug": slug}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_company", mock_update_company)

        await update_company(
            slug="acme",
            custom_fields=[
                CustomFieldValue(field_id=10, value="a"),
                CustomFieldValue(field_id=11, value="b"),
            ],
        )

        assert captured["patch"]["custom_fields"] == [
            {"field_id": 10, "value": "a"},
            {"field_id": 11, "value": "b"},
        ]


class TestSetCompanyCustomFieldsTool:
    @pytest.mark.anyio
    async def test_delegates_to_update_company(self, monkeypatch):
        captured: dict = {}

        async def mock_update_company(slug, patch):
            captured["slug"] = slug
            captured["patch"] = patch
            return {"slug": slug}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_company", mock_update_company)

        result = await set_company_custom_fields(
            slug="acme",
            fields=[CustomFieldValue(field_id=1, value="v")],
        )

        assert captured["slug"] == "acme"
        # Only custom_fields should be on the patch; no None-valued standard fields
        assert captured["patch"] == {"custom_fields": [{"field_id": 1, "value": "v"}]}
        assert isinstance(result, WriteResult)
        assert result.kind == "company"


# ---------------------------------------------------------------------------
# Contact write tools
# ---------------------------------------------------------------------------


class TestCreateContactTool:
    @pytest.mark.anyio
    async def test_builds_payload_and_returns_write_result(self, monkeypatch):
        captured: dict = {}

        async def mock_create_contact(payload):
            captured["payload"] = payload
            return {"slug": "jdoe"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_contact", mock_create_contact)

        result = await create_contact(
            first_name="Jane",
            last_name="Doe",
            email="j@x.com",
            company_slug="acme,widgets",
            custom_fields=[CustomFieldValue(field_id=1, value="v")],
        )

        payload = captured["payload"]
        assert payload["first_name"] == "Jane"
        assert payload["last_name"] == "Doe"
        assert payload["email"] == "j@x.com"
        assert payload["company_slug"] == "acme,widgets"
        assert payload["custom_fields"] == [{"field_id": 1, "value": "v"}]
        assert "stage_id" not in payload
        assert "owner_id" not in payload
        assert isinstance(result, WriteResult)
        assert result.kind == "contact"
        assert result.id == "jdoe"

    @pytest.mark.anyio
    async def test_omits_custom_fields_when_empty(self, monkeypatch):
        captured: dict = {}

        async def mock_create_contact(payload):
            captured["payload"] = payload
            return {"slug": "jdoe"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_contact", mock_create_contact)

        await create_contact(first_name="Jane", last_name="Doe")

        assert "custom_fields" not in captured["payload"]


class TestUpdateContactTool:
    @pytest.mark.anyio
    async def test_forwards_only_non_none_patch(self, monkeypatch):
        captured: dict = {}

        async def mock_update_contact(slug, patch):
            captured["slug"] = slug
            captured["patch"] = patch
            return {"slug": slug}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_contact", mock_update_contact)

        result = await update_contact(slug="jdoe", email="new@x.com")

        assert captured["slug"] == "jdoe"
        assert captured["patch"] == {"email": "new@x.com"}
        assert isinstance(result, WriteResult)
        assert result.kind == "contact"
        assert result.id == "jdoe"


class TestSetContactCustomFieldsTool:
    @pytest.mark.anyio
    async def test_delegates_to_update_contact(self, monkeypatch):
        captured: dict = {}

        async def mock_update_contact(slug, patch):
            captured["slug"] = slug
            captured["patch"] = patch
            return {"slug": slug}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_contact", mock_update_contact)

        result = await set_contact_custom_fields(
            slug="jdoe",
            fields=[CustomFieldValue(field_id=1, value="v")],
        )

        assert captured["slug"] == "jdoe"
        assert captured["patch"] == {"custom_fields": [{"field_id": 1, "value": "v"}]}
        assert isinstance(result, WriteResult)
        assert result.kind == "contact"


# ---------------------------------------------------------------------------
# Job write tools
# ---------------------------------------------------------------------------


class TestCreateJobTool:
    @pytest.mark.anyio
    async def test_builds_payload_with_required_fields(self, monkeypatch):
        captured: dict = {}

        async def mock_create_job(payload):
            captured["payload"] = payload
            return {"slug": "job-1", "name": "Eng"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_job", mock_create_job)

        result = await create_job(
            name="Eng",
            company_slug="acme",
            contact_slug="jdoe",
            number_of_openings=2,
            currency_id=1,
            enable_job_application_form=0,
            job_description_text="<p>desc</p>",
            job_status=1,
            job_location_type=1,
            min_annual_salary=100000,
            custom_fields=[CustomFieldValue(field_id=1, value="v")],
        )

        payload = captured["payload"]
        assert payload["name"] == "Eng"
        assert payload["company_slug"] == "acme"
        assert payload["contact_slug"] == "jdoe"
        assert payload["number_of_openings"] == 2
        assert payload["currency_id"] == 1
        assert payload["enable_job_application_form"] == 0
        assert payload["job_description_text"] == "<p>desc</p>"
        assert payload["job_status"] == 1
        assert payload["job_location_type"] == 1
        assert payload["min_annual_salary"] == 100000
        assert payload["custom_fields"] == [{"field_id": 1, "value": "v"}]
        # Optional fields omitted
        assert "city" not in payload
        assert "max_annual_salary" not in payload
        assert isinstance(result, WriteResult)
        assert result.kind == "job"
        assert result.id == "job-1"
        assert result.title == "Eng"

    @pytest.mark.anyio
    async def test_omits_custom_fields_when_empty(self, monkeypatch):
        captured: dict = {}

        async def mock_create_job(payload):
            captured["payload"] = payload
            return {"slug": "job-1"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_job", mock_create_job)

        await create_job(
            name="Eng",
            company_slug="acme",
            contact_slug="jdoe",
            number_of_openings=1,
            currency_id=1,
            enable_job_application_form=0,
            job_description_text="x",
        )

        assert "custom_fields" not in captured["payload"]


class TestUpdateJobTool:
    @pytest.mark.anyio
    async def test_forwards_only_non_none_patch(self, monkeypatch):
        captured: dict = {}

        async def mock_update_job(slug, patch):
            captured["slug"] = slug
            captured["patch"] = patch
            return {"slug": slug, "name": patch.get("name")}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_job", mock_update_job)

        result = await update_job(slug="job-1", name="Senior Eng", job_status=2)

        assert captured["slug"] == "job-1"
        assert captured["patch"] == {"name": "Senior Eng", "job_status": 2}
        assert isinstance(result, WriteResult)
        assert result.kind == "job"
        assert result.id == "job-1"


class TestSetJobCustomFieldsTool:
    @pytest.mark.anyio
    async def test_delegates_to_update_job(self, monkeypatch):
        captured: dict = {}

        async def mock_update_job(slug, patch):
            captured["slug"] = slug
            captured["patch"] = patch
            return {"slug": slug}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_job", mock_update_job)

        result = await set_job_custom_fields(
            slug="job-1",
            fields=[CustomFieldValue(field_id=1, value="v")],
        )

        assert captured["slug"] == "job-1"
        assert captured["patch"] == {"custom_fields": [{"field_id": 1, "value": "v"}]}
        assert isinstance(result, WriteResult)
        assert result.kind == "job"


# ---------------------------------------------------------------------------
# Candidate write tools
# ---------------------------------------------------------------------------


class TestCreateCandidateTool:
    @pytest.mark.anyio
    async def test_builds_payload_with_required_first_name(self, monkeypatch):
        captured: dict = {}

        async def mock_create_candidate(payload):
            captured["payload"] = payload
            return {"slug": "cand-1", "first_name": "Jane"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_candidate", mock_create_candidate)

        result = await create_candidate(
            first_name="Jane",
            last_name="Doe",
            email="j@x.com",
            position="Engineer",
            current_organization_slug="acme",
            custom_fields=[CustomFieldValue(field_id=1, value="v")],
        )

        payload = captured["payload"]
        assert payload["first_name"] == "Jane"
        assert payload["last_name"] == "Doe"
        assert payload["email"] == "j@x.com"
        assert payload["position"] == "Engineer"
        assert payload["current_organization_slug"] == "acme"
        assert payload["custom_fields"] == [{"field_id": 1, "value": "v"}]
        assert "notice_period" not in payload
        assert "available_from" not in payload
        assert isinstance(result, WriteResult)
        assert result.kind == "candidate"
        assert result.id == "cand-1"

    @pytest.mark.anyio
    async def test_omits_custom_fields_when_empty(self, monkeypatch):
        captured: dict = {}

        async def mock_create_candidate(payload):
            captured["payload"] = payload
            return {"slug": "cand-1"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_candidate", mock_create_candidate)

        await create_candidate(first_name="Jane")

        assert "custom_fields" not in captured["payload"]


class TestUpdateCandidateTool:
    @pytest.mark.anyio
    async def test_forwards_only_non_none_patch(self, monkeypatch):
        captured: dict = {}

        async def mock_update_candidate(slug, patch):
            captured["slug"] = slug
            captured["patch"] = patch
            return {"slug": slug, "position": patch.get("position")}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_candidate", mock_update_candidate)

        result = await update_candidate(slug="cand-1", position="Staff Engineer")

        assert captured["slug"] == "cand-1"
        assert captured["patch"] == {"position": "Staff Engineer"}
        assert isinstance(result, WriteResult)
        assert result.kind == "candidate"
        assert result.id == "cand-1"


class TestSetCandidateCustomFieldsTool:
    @pytest.mark.anyio
    async def test_delegates_to_update_candidate(self, monkeypatch):
        captured: dict = {}

        async def mock_update_candidate(slug, patch):
            captured["slug"] = slug
            captured["patch"] = patch
            return {"slug": slug}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_candidate", mock_update_candidate)

        result = await set_candidate_custom_fields(
            slug="cand-1",
            fields=[CustomFieldValue(field_id=1, value="v")],
        )

        assert captured["slug"] == "cand-1"
        assert captured["patch"] == {"custom_fields": [{"field_id": 1, "value": "v"}]}
        assert isinstance(result, WriteResult)
        assert result.kind == "candidate"


# ---------------------------------------------------------------------------
# Meeting update / note delete
# ---------------------------------------------------------------------------


class TestUpdateMeetingTool:
    @pytest.mark.anyio
    async def test_flattens_entity_ref_and_joins_attendees(self, monkeypatch):
        captured: dict = {}

        async def mock_update_meeting(meeting_id, patch):
            captured["meeting_id"] = meeting_id
            captured["patch"] = patch
            return {"id": meeting_id, "title": patch.get("title")}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_meeting", mock_update_meeting)

        result = await update_meeting(
            meeting_id=42,
            title="Updated",
            related_to=EntityRef(kind="candidate", id="cand-1"),
            attendee_contacts=["con-1", "con-2"],
            attendee_users=[99, 100],
            associated=Associations(jobs=["job-1"]),
        )

        patch = captured["patch"]
        assert captured["meeting_id"] == 42
        assert patch["title"] == "Updated"
        assert patch["related_to"] == "cand-1"
        assert patch["related_to_type"] == "candidate"
        assert patch["attendee_contacts"] == "con-1,con-2"
        assert patch["attendee_users"] == "99,100"
        assert patch["associated_jobs"] == "job-1"
        # Empty lists not present
        assert "attendee_candidates" not in patch
        assert "associated_candidates" not in patch
        assert "start_date" not in patch
        assert "description" not in patch
        assert isinstance(result, WriteResult)
        assert result.kind == "meeting"
        assert result.id == "42"

    @pytest.mark.anyio
    async def test_minimal_patch_only_forwards_id(self, monkeypatch):
        captured: dict = {}

        async def mock_update_meeting(meeting_id, patch):
            captured["meeting_id"] = meeting_id
            captured["patch"] = patch
            return {"id": meeting_id}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_meeting", mock_update_meeting)

        await update_meeting(meeting_id=7)

        assert captured["meeting_id"] == 7
        assert captured["patch"] == {}


class TestDeleteNoteTool:
    @pytest.mark.anyio
    async def test_calls_client_delete_and_returns_write_result(self, monkeypatch):
        captured: dict = {}

        async def mock_delete_note(note_id):
            captured["note_id"] = note_id
            return None

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "delete_note", mock_delete_note)

        result = await delete_note(note_id=42)

        assert captured["note_id"] == 42
        assert isinstance(result, WriteResult)
        assert result.kind == "note"
        assert result.id == "42"


# ---------------------------------------------------------------------------
# Assignment trio
# ---------------------------------------------------------------------------


class TestAssignCandidateTool:
    @pytest.mark.anyio
    async def test_assigns_and_returns_write_result(self, monkeypatch):
        captured: dict = {}

        async def mock_assign(candidate_slug, job_slug):
            captured["candidate_slug"] = candidate_slug
            captured["job_slug"] = job_slug
            return {"candidate_slug": "cand-1", "shared_list_url": "https://x.y/list"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "assign_candidate", mock_assign)

        result = await assign_candidate(candidate_slug="cand-1", job_slug="job-1")

        assert captured["candidate_slug"] == "cand-1"
        assert captured["job_slug"] == "job-1"
        assert isinstance(result, WriteResult)
        assert result.kind == "assignment"
        assert result.id == "cand-1"
        assert "cand-1" in result.title
        assert "job-1" in result.title
        assert result.url == "https://x.y/list"

    @pytest.mark.anyio
    async def test_falls_back_to_arg_when_response_has_no_slug(self, monkeypatch):
        async def mock_assign(candidate_slug, job_slug):
            return {}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "assign_candidate", mock_assign)

        result = await assign_candidate(candidate_slug="cand-1", job_slug="job-1")

        assert result.id == "cand-1"


class TestUnassignCandidateTool:
    @pytest.mark.anyio
    async def test_unassigns_and_returns_write_result(self, monkeypatch):
        captured: dict = {}

        async def mock_unassign(candidate_slug, job_slug):
            captured["candidate_slug"] = candidate_slug
            captured["job_slug"] = job_slug
            return {}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "unassign_candidate", mock_unassign)

        result = await unassign_candidate(candidate_slug="cand-1", job_slug="job-1")

        assert captured["candidate_slug"] == "cand-1"
        assert captured["job_slug"] == "job-1"
        assert isinstance(result, WriteResult)
        assert result.kind == "assignment"
        assert result.id == "cand-1"


class TestUpdateHiringStageTool:
    @pytest.mark.anyio
    async def test_forwards_body_and_returns_write_result(self, monkeypatch):
        captured: dict = {}

        async def mock_update_stage(candidate_slug, job_slug, body):
            captured["candidate_slug"] = candidate_slug
            captured["job_slug"] = job_slug
            captured["body"] = body
            return {"candidate_slug": candidate_slug, "status_id": body["status_id"]}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_hiring_stage", mock_update_stage)

        result = await update_hiring_stage(
            candidate_slug="cand-1",
            job_slug="job-1",
            status_id=5,
            remark="phone screen",
            stage_date="2025-04-29",
        )

        assert captured["candidate_slug"] == "cand-1"
        assert captured["job_slug"] == "job-1"
        assert captured["body"] == {
            "status_id": 5,
            "remark": "phone screen",
            "stage_date": "2025-04-29",
        }
        # create_placement omitted when None
        assert "create_placement" not in captured["body"]
        assert isinstance(result, WriteResult)
        assert result.kind == "assignment"
        assert result.id == "cand-1"
        assert "stage 5" in result.title

    @pytest.mark.anyio
    async def test_minimal_body_status_id_only(self, monkeypatch):
        captured: dict = {}

        async def mock_update_stage(candidate_slug, job_slug, body):
            captured["body"] = body
            return {}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_hiring_stage", mock_update_stage)

        await update_hiring_stage(
            candidate_slug="cand-1",
            job_slug="job-1",
            status_id=1,
        )

        assert captured["body"] == {"status_id": 1}


# ---------------------------------------------------------------------------
# File upload
# ---------------------------------------------------------------------------


class TestUploadFileTool:
    @pytest.mark.anyio
    async def test_unpacks_entity_ref_into_related_fields(self, monkeypatch):
        captured: dict = {}

        async def mock_upload(file_url, related_to, related_to_type, folder):
            captured["file_url"] = file_url
            captured["related_to"] = related_to
            captured["related_to_type"] = related_to_type
            captured["folder"] = folder
            return {"file_link": "https://cdn/x.pdf", "file_name": "x.pdf"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "upload_file", mock_upload)

        result = await upload_file(
            file_url="https://example.com/resume.pdf",
            related_to=EntityRef(kind="candidate", id="cand-1"),
            folder="Resumes",
        )

        assert captured["file_url"] == "https://example.com/resume.pdf"
        assert captured["related_to"] == "cand-1"
        assert captured["related_to_type"] == "candidate"
        assert captured["folder"] == "Resumes"
        assert isinstance(result, WriteResult)
        assert result.kind == "file"
        assert result.id == "https://cdn/x.pdf"
        assert result.title == "x.pdf"
        assert result.url == "https://cdn/x.pdf"

    @pytest.mark.anyio
    async def test_default_folder_is_uploads(self, monkeypatch):
        captured: dict = {}

        async def mock_upload(file_url, related_to, related_to_type, folder):
            captured["folder"] = folder
            return {"file_link": "https://x", "file_name": "x"}

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "upload_file", mock_upload)

        await upload_file(
            file_url="https://example.com/f.pdf",
            related_to=EntityRef(kind="company", id="co-1"),
        )

        assert captured["folder"] == "Uploads"


class TestWriteToolErrorSurfacing:
    """Write tools must translate ``RecruitCrmError`` into ``ToolError`` so MCP
    clients see a structured field-level message instead of the raw Python
    ``RuntimeError`` repr that FastMCP would otherwise stringify."""

    @pytest.mark.anyio
    async def test_create_note_surfaces_field_validation(self, monkeypatch):
        async def mock_create_note(payload):
            raise RecruitCrmError(
                422, {"description": ["field required"]}, "POST", "/notes"
            )

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_note", mock_create_note)

        with pytest.raises(ToolError) as excinfo:
            await create_note(
                description="",
                related_to=EntityRef(kind="candidate", id="cand-1"),
            )

        msg = str(excinfo.value)
        assert "422" in msg
        assert "description" in msg
        assert "field required" in msg

    @pytest.mark.anyio
    async def test_create_task_surfaces_field_validation(self, monkeypatch):
        async def mock_create_task(payload):
            raise RecruitCrmError(
                422, {"start_date": ["required"]}, "POST", "/tasks"
            )

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_task", mock_create_task)

        with pytest.raises(ToolError) as excinfo:
            await create_task(title="x", start_date="bogus")

        msg = str(excinfo.value)
        assert "422" in msg
        assert "start_date" in msg

    @pytest.mark.anyio
    async def test_log_meeting_surfaces_multiple_field_errors(self, monkeypatch):
        async def mock_create_meeting(payload):
            raise RecruitCrmError(
                422,
                {"title": ["required"], "end_date": ["must be after start"]},
                "POST",
                "/meetings",
            )

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "create_meeting", mock_create_meeting)

        with pytest.raises(ToolError) as excinfo:
            await log_meeting(
                title="",
                start_date="2025-05-01T09:00:00Z",
                end_date="2025-05-01T08:00:00Z",
                related_to=EntityRef(kind="candidate", id="cand-1"),
            )

        msg = str(excinfo.value)
        assert "422" in msg
        # Both field names must appear in the flattened message so the LLM
        # can see every problem in a single round-trip.
        assert "title" in msg
        assert "end_date" in msg

    @pytest.mark.anyio
    async def test_update_task_surfaces_field_validation(self, monkeypatch):
        async def mock_update_task(task_id, patch):
            raise RecruitCrmError(
                422, {"status": ["invalid value"]}, "POST", "/tasks/42"
            )

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_task", mock_update_task)

        with pytest.raises(ToolError) as excinfo:
            await update_task(task_id=42, status="bogus")

        msg = str(excinfo.value)
        assert "422" in msg
        assert "status" in msg
        assert "invalid value" in msg

    @pytest.mark.anyio
    async def test_update_meeting_surfaces_non_dict_body(self, monkeypatch):
        # Exercise the fallback branch where the API returns a plain string/None
        # body rather than a field-errors dict.
        async def mock_update_meeting(meeting_id, patch):
            raise RecruitCrmError(
                500, "Internal Server Error", "POST", "/meetings/99"
            )

        from recruit_crm_mcp import server
        monkeypatch.setattr(server.client, "update_meeting", mock_update_meeting)

        with pytest.raises(ToolError) as excinfo:
            await update_meeting(meeting_id=99, title="x")

        msg = str(excinfo.value)
        assert "500" in msg
        assert "Internal Server Error" in msg
