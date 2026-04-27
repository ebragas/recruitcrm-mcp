"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from recruit_crm_mcp.models import (
    AssignedCandidateSummary,
    Associations,
    CandidateSummary,
    CompanySummary,
    ContactSummary,
    CustomFieldValue,
    EntityRef,
    JobSummary,
    LookupItem,
    MeetingSummary,
    NoteSummary,
    TaskSummary,
    UserSummary,
    WriteResult,
)


# ---------------------------------------------------------------------------
# Summary model tests
# ---------------------------------------------------------------------------


class TestCandidateSummary:
    def test_from_api_response(self):
        data = {
            "slug": "cand-123",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "position": "Engineer",
            "current_organization": "Acme",
            "city": "Austin",
        }
        s = CandidateSummary.from_api_response(data)
        assert s.slug == "cand-123"
        assert s.name == "Jane Doe"
        assert s.email == "jane@example.com"
        assert s.position == "Engineer"
        assert s.company == "Acme"
        assert s.city == "Austin"

    def test_empty_dict(self):
        s = CandidateSummary.from_api_response({})
        assert s.slug is None
        assert s.name == ""
        assert s.email is None
        assert s.position is None
        assert s.company is None
        assert s.city is None


class TestJobSummary:
    def test_from_api_response(self):
        data = {
            "slug": "job-123",
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
        s = JobSummary.from_api_response(data)
        assert s.slug == "job-123"
        assert s.name == "Backend Engineer"
        assert s.status == "Open"
        assert s.city == "Austin"
        assert s.country == "US"
        assert s.job_type == "Full-time"
        assert s.job_location_type == "Remote"
        assert s.minimum_experience == "2"
        assert s.maximum_experience == "5"
        assert s.min_annual_salary == "80000"
        assert s.max_annual_salary == "120000"
        assert s.pay_rate == "0"
        assert s.bill_rate == "0"
        assert s.job_category == "Engineering"
        assert s.note_for_candidates == "Great team!"
        assert s.job_description_file is None

    def test_job_location_type_onsite(self):
        s = JobSummary.from_api_response({"job_location_type": "0"})
        assert s.job_location_type == "On-site"

    def test_job_location_type_hybrid(self):
        s = JobSummary.from_api_response({"job_location_type": "2"})
        assert s.job_location_type == "Hybrid"

    def test_job_location_type_unknown(self):
        s = JobSummary.from_api_response({"job_location_type": "99"})
        assert s.job_location_type == "99"

    def test_empty_dict(self):
        s = JobSummary.from_api_response({})
        assert s.slug is None
        assert s.name is None
        assert s.status is None
        assert s.job_location_type == ""


class TestContactSummary:
    def test_from_api_response(self):
        data = {
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
        s = ContactSummary.from_api_response(data)
        assert s.slug == "contact-123"
        assert s.name == "Jane Doe"
        assert s.email == "jane@example.com"
        assert s.contact_number == "+1234567890"
        assert s.designation == "VP Sales"
        assert s.company_slug == "acme-corp"
        assert s.city == "Austin"
        assert s.state == "Texas"
        assert s.country == "United States"
        assert s.linkedin == "https://linkedin.com/in/janedoe"

    def test_empty_dict(self):
        s = ContactSummary.from_api_response({})
        assert s.slug is None
        assert s.name == ""
        assert s.email is None
        assert s.contact_number is None
        assert s.designation is None
        assert s.company_slug is None
        assert s.city is None
        assert s.state is None
        assert s.country is None
        assert s.linkedin is None


class TestCompanySummary:
    def test_from_api_response(self):
        data = {
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
        s = CompanySummary.from_api_response(data)
        assert s.slug == "acme-corp"
        assert s.company_name == "Acme Corp"
        assert s.about_company == "A great company"
        assert s.website == "https://acme.com"
        assert s.city == "Austin"
        assert s.state == "Texas"
        assert s.country == "United States"
        assert s.linkedin == "https://linkedin.com/company/acme"
        assert s.industry_id == 42
        assert s.is_parent_company == 1
        assert s.is_child_company == 0

    def test_empty_dict(self):
        s = CompanySummary.from_api_response({})
        assert s.slug is None
        assert s.company_name is None
        assert s.about_company is None
        assert s.website is None
        assert s.city is None
        assert s.state is None
        assert s.country is None
        assert s.linkedin is None
        assert s.industry_id is None
        assert s.is_parent_company is None
        assert s.is_child_company is None


class TestNoteSummary:
    def test_from_api_response(self):
        data = {
            "id": 63590686,
            "note_type": {"id": 48622, "label": "Note"},
            "description": "Important note",
            "related_to": "cand-slug-123",
            "related_to_type": "candidate",
            "created_on": "2025-04-29T17:39:50.000000Z",
            "updated_on": "2025-04-29T17:55:30.000000Z",
        }
        s = NoteSummary.from_api_response(data)
        assert s.id == 63590686
        assert s.note_type == "Note"
        assert s.description == "Important note"
        assert s.related_to == "cand-slug-123"
        assert s.related_to_type == "candidate"
        assert s.created_on == "2025-04-29T17:39:50.000000Z"
        assert s.updated_on == "2025-04-29T17:55:30.000000Z"

    def test_empty_dict(self):
        s = NoteSummary.from_api_response({})
        assert s.id is None
        assert s.note_type is None
        assert s.description is None
        assert s.related_to is None
        assert s.related_to_type is None
        assert s.created_on is None
        assert s.updated_on is None


class TestTaskSummary:
    def test_from_api_response(self):
        data = {
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
        s = TaskSummary.from_api_response(data)
        assert s.id == 44261638
        assert s.title == "Follow up with Jane"
        assert s.task_type == "Call"
        assert s.status == 0
        assert s.start_date == "2025-04-29T18:30:00.000000Z"
        assert s.related_to == "cand-slug-123"
        assert s.related_to_type == "candidate"
        assert s.related_to_name == "Jane Doe"
        assert s.owner == 31585
        assert s.reminder_date == "2025-04-29T18:00:00.000000Z"

    def test_null_task_type(self):
        s = TaskSummary.from_api_response({"task_type": None})
        assert s.task_type is None

    def test_empty_dict(self):
        s = TaskSummary.from_api_response({})
        assert s.id is None
        assert s.title is None
        assert s.task_type is None
        assert s.status is None
        assert s.start_date is None
        assert s.related_to is None
        assert s.related_to_type is None
        assert s.related_to_name is None
        assert s.owner is None
        assert s.reminder_date is None


class TestMeetingSummary:
    def test_from_api_response(self):
        data = {
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
        s = MeetingSummary.from_api_response(data)
        assert s.id == 37639022
        assert s.title == "Interview with Jane"
        assert s.meeting_type == "Candidate Interview"
        assert s.status == 0
        assert s.start_date == "2025-04-29T18:30:00.000000Z"
        assert s.end_date == "2025-04-29T19:00:00.000000Z"
        assert s.all_day == 0
        assert s.address == "123 Main St"
        assert s.related_to == "cand-slug-123"
        assert s.related_to_type == "candidate"
        assert s.owner == 31585

    def test_empty_dict(self):
        s = MeetingSummary.from_api_response({})
        assert s.id is None
        assert s.title is None
        assert s.meeting_type is None
        assert s.status is None
        assert s.start_date is None
        assert s.end_date is None
        assert s.all_day is None
        assert s.address is None
        assert s.related_to is None
        assert s.related_to_type is None
        assert s.owner is None


class TestUserSummary:
    def test_from_api_response(self):
        data = {
            "id": 43135,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "role": "Admin",
        }
        s = UserSummary.from_api_response(data)
        assert s.id == 43135
        assert s.name == "Jane Doe"
        assert s.email == "jane@example.com"
        assert s.role == "Admin"

    def test_empty_dict(self):
        s = UserSummary.from_api_response({})
        assert s.id is None
        assert s.name == ""
        assert s.email is None
        assert s.role is None


class TestAssignedCandidateSummary:
    def test_from_api_response(self):
        data = {
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
        }
        s = AssignedCandidateSummary.from_api_response(data)
        assert s.slug == "cand-123"
        assert s.name == "Jane Doe"
        assert s.email == "jane@example.com"
        assert s.position == "Engineer"
        assert s.company == "Acme"
        assert s.city == "Austin"
        assert s.hiring_status == "Interview"

    def test_missing_status(self):
        data = {
            "candidate": {"slug": "cand-456", "first_name": "John", "last_name": "Smith"},
        }
        s = AssignedCandidateSummary.from_api_response(data)
        assert s.slug == "cand-456"
        assert s.name == "John Smith"
        assert s.hiring_status is None

    def test_empty_dict(self):
        s = AssignedCandidateSummary.from_api_response({})
        assert s.slug is None
        assert s.name == ""
        assert s.hiring_status is None


# ---------------------------------------------------------------------------
# Input model tests
# ---------------------------------------------------------------------------


class TestEntityRef:
    def test_accepts_all_kinds(self):
        for kind in ("candidate", "company", "contact", "job", "deal"):
            ref = EntityRef(kind=kind, id="some-id")
            assert ref.kind == kind
            assert ref.id == "some-id"

    def test_rejects_invalid_kind(self):
        with pytest.raises(ValidationError):
            EntityRef(kind="bogus", id="some-id")

    def test_extra_field_rejected(self):
        with pytest.raises(ValidationError):
            EntityRef(kind="candidate", id="cand-123", bogus="nope")


class TestAssociations:
    def test_defaults(self):
        a = Associations()
        assert a.candidates == []
        assert a.companies == []
        assert a.contacts == []
        assert a.jobs == []
        assert a.deals == []

    def test_populated(self):
        a = Associations(
            candidates=["cand-1"],
            companies=["comp-1"],
            contacts=["cont-1"],
            jobs=["job-1"],
            deals=["deal-1"],
        )
        assert a.candidates == ["cand-1"]
        assert a.deals == ["deal-1"]

    def test_extra_field_rejected(self):
        with pytest.raises(ValidationError):
            Associations(unknown=["x"])


class TestLookupItem:
    def test_from_api_response_normal(self):
        item = LookupItem.from_api_response({"id": 42, "label": "Call"})
        assert item.id == 42
        assert item.label == "Call"

    def test_from_api_response_missing_label(self):
        item = LookupItem.from_api_response({"id": 7})
        assert item.id == 7
        assert item.label == ""

    def test_from_api_response_null_label(self):
        item = LookupItem.from_api_response({"id": 7, "label": None})
        assert item.id == 7
        assert item.label == ""


class TestWriteResult:
    def test_valid_kind(self):
        r = WriteResult(kind="note", id="63590686", title="A note")
        assert r.kind == "note"
        assert r.id == "63590686"
        assert r.title == "A note"
        assert r.url is None

    def test_invalid_kind_rejected(self):
        with pytest.raises(ValidationError):
            WriteResult(kind="bogus", id="123")

    def test_file_kind_accepted(self):
        """``file`` is a valid WriteKind for upload_file results."""
        r = WriteResult(
            kind="file",
            id="https://cdn/x.pdf",
            title="x.pdf",
            url="https://cdn/x.pdf",
        )
        assert r.kind == "file"
        assert r.id == "https://cdn/x.pdf"
        assert r.url == "https://cdn/x.pdf"


class TestCustomFieldValue:
    def test_required_fields(self):
        cf = CustomFieldValue(field_id=1, value="Enterprise")
        assert cf.field_id == 1
        assert cf.value == "Enterprise"

    def test_missing_field_id_raises(self):
        with pytest.raises(ValidationError):
            CustomFieldValue(value="x")

    def test_missing_value_raises(self):
        with pytest.raises(ValidationError):
            CustomFieldValue(field_id=1)

    def test_extra_field_rejected(self):
        with pytest.raises(ValidationError):
            CustomFieldValue(field_id=1, value="x", bogus="nope")

    def test_round_trip(self):
        cf = CustomFieldValue(field_id=42, value="Hello")
        d = cf.model_dump()
        assert d == {"field_id": 42, "value": "Hello"}
        cf2 = CustomFieldValue.model_validate(d)
        assert cf2 == cf
