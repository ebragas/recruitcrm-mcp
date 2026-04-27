"""Integration tests against the live Recruit CRM API.

Requires RECRUIT_CRM_API_KEY in environment (loaded from .env via pytest-dotenv).
Run with: make integration-test
"""

import os
from datetime import datetime, timezone

import pytest

from recruit_crm_mcp import client
from recruit_crm_mcp.client import RecruitCrmError
from recruit_crm_mcp.models import (
    CandidateSummary,
    CompanySummary,
    ContactSummary,
    JobSummary,
    LookupItem,
    MeetingSummary,
    NoteSummary,
    TaskSummary,
    UserSummary,
)
from tests.integration.conftest import _test_label


def _parse_dt(value: str) -> datetime:
    """Parse an ISO timestamp into a timezone-aware UTC datetime."""
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

pytestmark = [
    pytest.mark.anyio,
    pytest.mark.integration,
    pytest.mark.skipif(
        not os.environ.get("RECRUIT_CRM_API_KEY"),
        reason="RECRUIT_CRM_API_KEY not set",
    ),
]


class TestCandidates:
    async def test_search_returns_results(self):
        results = await client.search_candidates(limit=3)
        assert len(results) > 0

    async def test_search_results_have_expected_fields(self):
        results = await client.search_candidates(limit=1)
        candidate = results[0]
        assert "slug" in candidate
        assert "first_name" in candidate
        assert "last_name" in candidate
        assert "position" in candidate
        assert "current_organization" in candidate

    async def test_summarize_candidate_from_live_data(self):
        results = await client.search_candidates(limit=1)
        summary = CandidateSummary.from_api_response(results[0])
        assert summary.slug is not None
        assert summary.name  # non-empty

    async def test_get_candidate_by_slug(self):
        results = await client.search_candidates(limit=1)
        slug = results[0]["slug"]
        candidate = await client.get_candidate(slug)
        assert candidate["slug"] == slug
        assert "first_name" in candidate

    async def test_candidate_resume_field_structure(self):
        results = await client.search_candidates(limit=5)
        # Find a candidate with a resume
        for r in results:
            candidate = await client.get_candidate(r["slug"])
            resume = candidate.get("resume")
            if resume:
                assert isinstance(resume, dict)
                assert "filename" in resume
                assert "file_link" in resume
                return
        pytest.skip("No candidates with resumes found in first 5 results")


class TestSearchCandidateFilters:
    """Integration tests for /candidates/search filter parameters."""

    async def test_country_filter_returns_matching_results(self):
        """All results from a country filter should contain the search term.

        Note: the API uses fuzzy/contains matching on country (e.g. searching
        "United States" also matches "United States of America").
        """
        # Discover a country value from existing data
        candidates = await client.search_candidates(limit=5)
        country = next((c["country"] for c in candidates if c.get("country")), None)
        if not country:
            pytest.skip("No candidates with country populated")

        results = await client.search_candidates(country=country, limit=10)
        assert len(results) > 0
        for r in results:
            assert country.lower() in r["country"].lower(), (
                f"Expected country containing {country!r}, got {r['country']!r}"
            )

    async def test_state_filter_returns_matching_results(self):
        """All results from a state filter should have that state."""
        candidates = await client.search_candidates(limit=10)
        state = next((c["state"] for c in candidates if c.get("state")), None)
        if not state:
            pytest.skip("No candidates with state populated")

        results = await client.search_candidates(state=state, limit=10)
        assert len(results) > 0
        for r in results:
            assert r["state"] == state, (
                f"Expected state {state!r}, got {r['state']!r}"
            )

    async def test_date_filter_created_from(self):
        """created_from filter should only return candidates created on or after that date."""
        # Derive cutoff from existing data to avoid flakiness
        candidates = await client.search_candidates(limit=1)
        if not candidates or not candidates[0].get("created_on"):
            pytest.skip("No candidates with created_on populated")
        cutoff = candidates[0]["created_on"][:10]  # YYYY-MM-DD
        results = await client.search_candidates(created_from=cutoff, limit=10)
        if not results:
            pytest.skip("No candidates found matching created_from filter")
        cutoff_dt = datetime.fromisoformat(cutoff).replace(tzinfo=timezone.utc)
        for r in results:
            created_on = r.get("created_on")
            assert created_on, f"Candidate {r.get('slug')} missing created_on"
            dt = _parse_dt(created_on)
            assert dt >= cutoff_dt, (
                f"Candidate created_on {created_on} is before cutoff {cutoff}"
            )

    async def test_date_filter_created_to(self):
        """created_to filter should only return candidates created on or before that date."""
        # Use a date in the past so we get bounded results
        cutoff = "2025-12-31"
        results = await client.search_candidates(created_to=cutoff, limit=10)
        if not results:
            pytest.skip("No candidates created before cutoff date")
        cutoff_dt = datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        for r in results:
            created_on = r.get("created_on")
            assert created_on, f"Candidate {r.get('slug')} missing created_on"
            dt = _parse_dt(created_on)
            assert dt <= cutoff_dt, (
                f"Candidate created_on {created_on} is after cutoff {cutoff}"
            )

    async def test_combined_country_and_state_filter(self):
        """Combining country + state should narrow results to match both.

        Note: the API uses fuzzy/contains matching on country (e.g. searching
        "United States" also matches "United States of America"), so we only
        assert exact match on state and verify country contains the search term.
        """
        # Discover values via the state filter (exact match).
        candidates = await client.search_candidates(state="New York", limit=5)
        if not candidates:
            pytest.skip("No candidates in state 'New York'")
        country_value = candidates[0].get("country")
        if not country_value:
            pytest.skip("Candidate in New York has no country set")

        results = await client.search_candidates(
            country=country_value, state="New York", limit=10,
        )
        assert len(results) > 0
        for r in results:
            assert r["state"] == "New York", (
                f"Expected state 'New York', got {r['state']!r}"
            )
            # Country filter is fuzzy — verify the search term appears in the result
            assert country_value.lower() in r["country"].lower(), (
                f"Expected country containing {country_value!r}, got {r['country']!r}"
            )

    async def test_sort_by_rejected_on_search_endpoint(self):
        """The API rejects sort_by/sort_order on /candidates/search with 422."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get(
                "/candidates/search",
                {"country": "United States", "sort_by": "updated_at"},
            )
        assert exc_info.value.status == 422

    async def test_sort_by_rejected_on_list_endpoint(self):
        """The API rejects sort_by/sort_order on /candidates with 422."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get(
                "/candidates",
                {"limit": 1, "sort_by": "updated_at", "sort_order": "desc"},
            )
        assert exc_info.value.status == 422

    async def test_no_filters_fallback_succeeds(self):
        """Calling search_candidates with no filters should not 422."""
        results = await client.search_candidates(limit=3)
        assert len(results) > 0


class TestListJobs:
    async def test_list_returns_results(self):
        results = await client.list_jobs(limit=3)
        assert len(results) > 0

    async def test_job_results_have_expected_fields(self):
        results = await client.list_jobs(limit=1)
        job = results[0]
        assert "slug" in job
        assert "name" in job
        assert "job_status" in job

    async def test_job_status_is_object(self):
        results = await client.list_jobs(limit=1)
        job_status = results[0]["job_status"]
        assert isinstance(job_status, dict)
        assert "id" in job_status
        assert "label" in job_status

    async def test_summarize_job_from_live_data(self):
        results = await client.list_jobs(limit=1)
        summary = JobSummary.from_api_response(results[0])
        assert summary.slug is not None
        assert summary.name
        assert summary.status  # should resolve from job_status.label

    async def test_get_job_by_slug(self):
        results = await client.list_jobs(limit=1)
        slug = results[0]["slug"]
        job = await client.get_job(slug)
        assert job["slug"] == slug
        assert "name" in job
        assert "job_description_text" in job

    async def test_job_response_has_expanded_fields(self):
        """Job records should contain the expanded response fields."""
        results = await client.list_jobs(limit=1)
        job = results[0]
        for field in [
            "job_location_type",
            "minimum_experience",
            "maximum_experience",
            "min_annual_salary",
            "max_annual_salary",
            "pay_rate",
            "bill_rate",
            "job_category",
            "note_for_candidates",
            "job_description_file",
        ]:
            assert field in job, f"Expected field {field!r} missing from job record"


class TestSearchJobs:
    """Regression tests for MAIN-87: status filter was silently ignored."""

    async def test_search_open_returns_only_open(self):
        results = await client.search_jobs(status="Open", limit=25)
        assert len(results) > 0
        for j in results:
            status = j.get("job_status", {})
            assert isinstance(status, dict)
            assert status.get("label") == "Open", (
                f"Expected status 'Open', got {status.get('label')!r}"
            )

    async def test_search_canceled_returns_only_canceled(self):
        # Note: "Closed" has status ID 0, which the API treats as no-filter.
        # Use "Canceled" (ID 3) instead for this test.
        results = await client.search_jobs(status="Canceled", limit=25)
        assert len(results) > 0
        for j in results:
            status = j.get("job_status", {})
            assert status.get("label") == "Canceled", (
                f"Expected status 'Canceled', got {status.get('label')!r}"
            )

    async def test_different_statuses_return_different_results(self):
        """Core MAIN-87 regression: different status filters must NOT
        return identical result sets."""
        open_jobs = await client.search_jobs(status="Open", limit=10)
        canceled_jobs = await client.search_jobs(status="Canceled", limit=10)

        if open_jobs and canceled_jobs:
            slugs_open = {j["slug"] for j in open_jobs}
            slugs_canceled = {j["slug"] for j in canceled_jobs}
            assert slugs_open != slugs_canceled, (
                "Different status filters returned identical results — "
                "filters are likely being ignored"
            )

    async def test_search_no_filters_returns_empty(self):
        results = await client.search_jobs()
        assert results == []


class TestSearchJobFilters:
    """Integration tests for /jobs/search date and owner filters."""

    async def test_created_from_filter(self):
        """created_from filter should only return jobs created on or after that date."""
        # Derive cutoff from existing data to avoid flakiness
        jobs = await client.list_jobs(limit=1)
        if not jobs or not jobs[0].get("created_on"):
            pytest.skip("No jobs with created_on populated")
        cutoff = jobs[0]["created_on"][:10]  # YYYY-MM-DD
        results = await client.search_jobs(created_from=cutoff, limit=10)
        if not results:
            pytest.skip("No jobs found matching created_from filter")
        cutoff_dt = datetime.fromisoformat(cutoff).replace(tzinfo=timezone.utc)
        for j in results:
            created_on = j.get("created_on")
            assert created_on, f"Job {j.get('slug')} missing created_on"
            dt = _parse_dt(created_on)
            assert dt >= cutoff_dt, (
                f"Job created_on {created_on} is before cutoff {cutoff}"
            )

    async def test_updated_from_filter(self):
        """updated_from filter should only return jobs updated on or after that date."""
        # Derive cutoff from existing data to avoid flakiness
        jobs = await client.list_jobs(limit=1)
        if not jobs or not jobs[0].get("updated_on"):
            pytest.skip("No jobs with updated_on populated")
        cutoff = jobs[0]["updated_on"][:10]  # YYYY-MM-DD
        results = await client.search_jobs(updated_from=cutoff, limit=10)
        if not results:
            pytest.skip("No jobs found matching updated_from filter")
        cutoff_dt = datetime.fromisoformat(cutoff).replace(tzinfo=timezone.utc)
        for j in results:
            updated_on = j.get("updated_on")
            assert updated_on, f"Job {j.get('slug')} missing updated_on"
            dt = _parse_dt(updated_on)
            assert dt >= cutoff_dt, (
                f"Job updated_on {updated_on} is before cutoff {cutoff}"
            )

    async def test_owner_id_filter(self):
        """owner_id filter should only return jobs with matching owner."""
        # Discover a valid owner ID from existing jobs
        jobs = await client.list_jobs(limit=5)
        owner = next((j["owner"] for j in jobs if j.get("owner")), None)
        if not owner:
            pytest.skip("No jobs with owner populated")

        results = await client.search_jobs(owner_id=owner, limit=10)
        assert len(results) > 0
        for j in results:
            assert j["owner"] == owner, (
                f"Expected owner {owner}, got {j['owner']}"
            )

    async def test_created_on_rejected(self):
        """The API rejects created_on param with 400."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get("/jobs/search", {"created_on": "2025-01-01"})
        assert exc_info.value.status == 400

    async def test_updated_on_rejected(self):
        """The API rejects updated_on param with 400."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get("/jobs/search", {"updated_on": "2025-01-01"})
        assert exc_info.value.status == 400

    async def test_owner_rejected(self):
        """The API rejects owner param (not owner_id) with 400."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get("/jobs/search", {"owner": 1})
        assert exc_info.value.status == 400


class TestGetAssignedCandidates:
    """Integration tests for GET /jobs/{slug}/assigned-candidates."""

    async def test_returns_results(self):
        """Find a job with assigned candidates and verify non-empty results."""
        jobs = await client.list_jobs(limit=5)
        for job in jobs:
            results = await client.get_assigned_candidates(job["slug"], limit=5)
            if results:
                return
        pytest.skip("No jobs with assigned candidates found in first 5 jobs")

    async def test_result_has_candidate_and_status(self):
        """Each result item should have candidate and status keys."""
        jobs = await client.list_jobs(limit=5)
        for job in jobs:
            results = await client.get_assigned_candidates(job["slug"], limit=5)
            if results:
                for item in results:
                    assert "candidate" in item, "Result missing 'candidate' key"
                    assert "status" in item, "Result missing 'status' key"
                return
        pytest.skip("No jobs with assigned candidates found in first 5 jobs")

    async def test_status_id_filter(self):
        """Filter by a discovered status_id and verify all results match."""
        jobs = await client.list_jobs(limit=5)
        for job in jobs:
            results = await client.get_assigned_candidates(job["slug"], limit=5)
            if results:
                # Discover a status_id from the first result
                status = results[0].get("status", {})
                sid = status.get("id")
                if sid is None:
                    continue
                filtered = await client.get_assigned_candidates(
                    job["slug"], status_id=str(sid), limit=25,
                )
                assert len(filtered) > 0
                for item in filtered:
                    assert item["status"]["id"] == sid, (
                        f"Expected status_id {sid}, got {item['status']['id']}"
                    )
                return
        pytest.skip("No jobs with assigned candidates and status_id found")


class TestListUsers:
    """Integration tests for /users endpoint."""

    async def test_list_returns_users(self):
        results = await client.list_users()
        assert len(results) > 0

    async def test_user_has_expected_fields(self):
        results = await client.list_users()
        user = results[0]
        for field in ["id", "first_name", "last_name", "role"]:
            assert field in user, f"Expected field {field!r} missing from user record"

    async def test_summarize_user_from_live_data(self):
        results = await client.list_users()
        summary = UserSummary.from_api_response(results[0])
        assert summary.id is not None
        assert summary.name
        # email may be None for some users — attribute always exists on the model


class TestContacts:
    """Raw API probes for contacts endpoints."""

    # Shared cache to avoid redundant API calls (rate limit is 60/min).
    _cached_contacts: list[dict] | None = None

    async def _get_contacts(self) -> list[dict]:
        if TestContacts._cached_contacts is None:
            data = await client.get("/contacts", {"limit": 10})
            TestContacts._cached_contacts = client._extract_results(data)
        return TestContacts._cached_contacts

    async def test_list_returns_results(self):
        """GET /contacts with limit returns non-empty results."""
        contacts = await self._get_contacts()
        assert len(contacts) > 0

    async def test_contact_has_expected_fields(self):
        """Verify field names on a contact record."""
        contacts = await self._get_contacts()
        contact = contacts[0]
        for field in [
            "slug", "first_name", "last_name", "email",
            "contact_number", "designation", "city", "state", "country",
        ]:
            assert field in contact, f"Expected field {field!r} missing from contact"

    async def test_get_contact_by_slug(self):
        """GET /contacts/{slug} returns the matching contact."""
        contacts = await self._get_contacts()
        slug = contacts[0]["slug"]
        contact = await client.get(f"/contacts/{slug}")
        assert contact["slug"] == slug
        assert "first_name" in contact

    async def test_search_no_filters_returns_empty(self):
        """/contacts/search with no params returns []."""
        data = await client.get("/contacts/search")
        results = client._extract_results(data)
        assert results == []

    async def test_email_filter(self):
        """Discover an email from listing, then filter by it."""
        contacts = await self._get_contacts()
        email = next((c["email"] for c in contacts if c.get("email")), None)
        if not email:
            pytest.skip("No contacts with email populated")

        data = await client.get("/contacts/search", {"email": email})
        results = client._extract_results(data)
        assert len(results) > 0
        assert any(r["email"] == email for r in results)

    async def test_first_name_filter(self):
        """Discover a first_name, then filter by it."""
        contacts = await self._get_contacts()
        name = next((c["first_name"] for c in contacts if c.get("first_name")), None)
        if not name:
            pytest.skip("No contacts with first_name populated")

        data = await client.get("/contacts/search", {"first_name": name})
        results = client._extract_results(data)
        assert len(results) > 0

    async def test_company_slug_filter(self):
        """Discover a company_slug, filter, and verify all results match."""
        contacts = await self._get_contacts()
        company_slug = next(
            (c["company_slug"] for c in contacts if c.get("company_slug")), None,
        )
        if not company_slug:
            pytest.skip("No contacts with company_slug populated")

        data = await client.get("/contacts/search", {"company_slug": company_slug})
        results = client._extract_results(data)
        assert len(results) > 0
        for r in results:
            assert r["company_slug"] == company_slug

    async def test_created_from_filter(self):
        """created_from filter should only return contacts created on/after that date."""
        contacts = await self._get_contacts()
        if not contacts or not contacts[0].get("created_on"):
            pytest.skip("No contacts with created_on populated")
        cutoff = contacts[0]["created_on"][:10]
        data = await client.get("/contacts/search", {"created_from": cutoff})
        results = client._extract_results(data)
        if not results:
            pytest.skip("No contacts found matching created_from filter")
        cutoff_dt = datetime.fromisoformat(cutoff).replace(tzinfo=timezone.utc)
        for r in results:
            created_on = r.get("created_on")
            assert created_on, f"Contact {r.get('slug')} missing created_on"
            dt = _parse_dt(created_on)
            assert dt >= cutoff_dt

    async def test_owner_id_filter(self):
        """Discover an owner, filter, verify all results match."""
        contacts = await self._get_contacts()
        owner = next((c["owner"] for c in contacts if c.get("owner")), None)
        if not owner:
            pytest.skip("No contacts with owner populated")

        data = await client.get("/contacts/search", {"owner_id": owner})
        results = client._extract_results(data)
        assert len(results) > 0
        for r in results:
            assert r["owner"] == owner

    async def test_designation_rejected(self):
        """The API rejects designation param on /contacts/search with 400."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get("/contacts/search", {"designation": "VP Sales"})
        assert exc_info.value.status == 400


class TestSearchContacts:
    """High-level integration tests using client functions."""

    async def test_no_filters_returns_results(self):
        results = await client.search_contacts(limit=3)
        assert len(results) > 0

    async def test_results_have_expected_fields(self):
        results = await client.search_contacts(limit=1)
        contact = results[0]
        assert "slug" in contact
        assert "first_name" in contact
        assert "email" in contact

    async def test_get_contact_by_slug(self):
        results = await client.search_contacts(limit=1)
        slug = results[0]["slug"]
        contact = await client.get_contact(slug)
        assert contact["slug"] == slug
        assert "first_name" in contact

    async def test_summarize_contact_from_live_data(self):
        results = await client.search_contacts(limit=1)
        summary = ContactSummary.from_api_response(results[0])
        assert summary.slug is not None
        assert summary.name


class TestMeetings:
    """Raw API probes for meetings endpoints."""

    _cached_meetings: list[dict] | None = None

    async def _get_meetings(self) -> list[dict]:
        if TestMeetings._cached_meetings is None:
            data = await client.get("/meetings/search", {"starting_from": "2020-01-01"})
            TestMeetings._cached_meetings = client._extract_results(data)
        return TestMeetings._cached_meetings

    async def test_search_no_filters_returns_empty(self):
        """/meetings/search with no params returns []."""
        data = await client.get("/meetings/search")
        results = client._extract_results(data)
        assert results == []

    async def test_list_endpoint_exists(self):
        """GET /meetings with limit returns results."""
        data = await client.get("/meetings", {"limit": 3})
        results = client._extract_results(data)
        assert isinstance(results, list)
        assert len(results) > 0

    async def test_meeting_has_expected_fields(self):
        """Verify field names from a meeting record.

        Note: meetings use 'id' (integer) not 'slug'.
        """
        meetings = await self._get_meetings()
        if not meetings:
            pytest.skip("No meetings found")
        meeting = meetings[0]
        for field in [
            "id", "title", "meeting_type", "status",
            "start_date", "end_date", "all_day", "address",
            "related_to", "related_to_type", "owner",
        ]:
            assert field in meeting, f"Expected field {field!r} missing from meeting"

    async def test_get_meeting_by_id(self):
        """GET /meetings/{id} returns the matching meeting."""
        meetings = await self._get_meetings()
        if not meetings:
            pytest.skip("No meetings found")
        meeting_id = meetings[0]["id"]
        meeting = await client.get(f"/meetings/{meeting_id}")
        assert meeting["id"] == meeting_id

    async def test_title_filter(self):
        """Discover a title from listing, then filter by it."""
        meetings = await self._get_meetings()
        title = next((m["title"] for m in meetings if m.get("title")), None)
        if not title:
            pytest.skip("No meetings with title populated")

        data = await client.get("/meetings/search", {"title": title})
        results = client._extract_results(data)
        assert len(results) > 0

    async def test_created_from_filter(self):
        """created_from filter should only return meetings created on/after that date."""
        meetings = await self._get_meetings()
        if not meetings or not meetings[0].get("created_on"):
            pytest.skip("No meetings with created_on populated")
        cutoff = meetings[0]["created_on"][:10]
        data = await client.get("/meetings/search", {"created_from": cutoff})
        results = client._extract_results(data)
        if not results:
            pytest.skip("No meetings found matching created_from filter")
        cutoff_dt = datetime.fromisoformat(cutoff).replace(tzinfo=timezone.utc)
        for r in results:
            created_on = r.get("created_on")
            assert created_on, f"Meeting {r.get('id')} missing created_on"
            dt = _parse_dt(created_on)
            assert dt >= cutoff_dt

    async def test_starting_from_filter(self):
        """starting_from filter should return meetings starting on/after that date."""
        meetings = await self._get_meetings()
        if not meetings or not meetings[0].get("start_date"):
            pytest.skip("No meetings with start_date populated")
        cutoff = meetings[0]["start_date"][:10]
        data = await client.get("/meetings/search", {"starting_from": cutoff})
        results = client._extract_results(data)
        assert len(results) > 0

    async def test_owner_id_filter(self):
        """Discover an owner, filter, verify all results match."""
        meetings = await self._get_meetings()
        owner = next((m["owner"] for m in meetings if m.get("owner")), None)
        if not owner:
            pytest.skip("No meetings with owner populated")

        data = await client.get("/meetings/search", {"owner_id": owner})
        results = client._extract_results(data)
        assert len(results) > 0
        for r in results:
            assert r["owner"] == owner

    async def test_related_to_rejected(self):
        """The API rejects related_to param on /meetings/search with 422."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get("/meetings/search", {"related_to": "test-slug"})
        assert exc_info.value.status == 422

    async def test_related_to_type_rejected(self):
        """The API rejects related_to_type param on /meetings/search with 422."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get("/meetings/search", {"related_to_type": "candidate"})
        assert exc_info.value.status == 422


class TestSearchMeetings:
    """High-level integration tests using client functions."""

    async def test_search_returns_results(self):
        results = await client.search_meetings(limit=3)
        assert len(results) > 0

    async def test_results_have_expected_fields(self):
        results = await client.search_meetings(limit=1)
        meeting = results[0]
        assert "id" in meeting
        assert "title" in meeting
        assert "meeting_type" in meeting

    async def test_get_meeting_by_id(self):
        results = await client.search_meetings(limit=1)
        meeting_id = results[0]["id"]
        meeting = await client.get_meeting(meeting_id)
        assert meeting["id"] == meeting_id
        assert "title" in meeting

    async def test_summarize_meeting_from_live_data(self):
        results = await client.search_meetings(limit=1)
        summary = MeetingSummary.from_api_response(results[0])
        assert summary.id is not None
        assert summary.title


class TestCompanies:
    """Raw API probes for companies endpoints."""

    _cached_companies: list[dict] | None = None

    async def _get_companies(self) -> list[dict]:
        if TestCompanies._cached_companies is None:
            data = await client.get("/companies", {"limit": 10})
            TestCompanies._cached_companies = client._extract_results(data)
        return TestCompanies._cached_companies

    async def test_list_returns_results(self):
        """GET /companies with limit returns non-empty results."""
        companies = await self._get_companies()
        assert len(companies) > 0

    async def test_company_has_expected_fields(self):
        """Verify field names on a company record."""
        companies = await self._get_companies()
        company = companies[0]
        for field in [
            "slug", "company_name", "about_company", "website",
            "city", "state", "country", "linkedin",
        ]:
            assert field in company, f"Expected field {field!r} missing from company"

    async def test_get_company_by_slug(self):
        """GET /companies/{slug} returns the matching company."""
        companies = await self._get_companies()
        slug = companies[0]["slug"]
        company = await client.get(f"/companies/{slug}")
        assert company["slug"] == slug
        assert "company_name" in company

    async def test_search_no_filters_returns_empty(self):
        """/companies/search with no params returns []."""
        data = await client.get("/companies/search")
        results = client._extract_results(data)
        assert results == []

    async def test_company_name_filter(self):
        """Discover a company_name, then filter by it."""
        companies = await self._get_companies()
        name = next((c["company_name"] for c in companies if c.get("company_name")), None)
        if not name:
            pytest.skip("No companies with company_name populated")

        data = await client.get("/companies/search", {"company_name": name})
        results = client._extract_results(data)
        assert len(results) > 0

    async def test_created_from_filter(self):
        """created_from filter should return companies created on/after that date."""
        companies = await self._get_companies()
        if not companies or not companies[0].get("created_on"):
            pytest.skip("No companies with created_on populated")
        cutoff = companies[0]["created_on"][:10]
        data = await client.get("/companies/search", {"created_from": cutoff})
        results = client._extract_results(data)
        if not results:
            pytest.skip("No companies found matching created_from filter")
        cutoff_dt = datetime.fromisoformat(cutoff).replace(tzinfo=timezone.utc)
        for r in results:
            created_on = r.get("created_on")
            assert created_on, f"Company {r.get('slug')} missing created_on"
            dt = _parse_dt(created_on)
            assert dt >= cutoff_dt

    async def test_owner_id_filter(self):
        """Discover an owner, filter, verify all results match."""
        companies = await self._get_companies()
        owner = next((c["owner"] for c in companies if c.get("owner")), None)
        if not owner:
            pytest.skip("No companies with owner populated")

        data = await client.get("/companies/search", {"owner_id": owner})
        results = client._extract_results(data)
        assert len(results) > 0
        for r in results:
            assert r["owner"] == owner

    async def test_sort_by_filter(self):
        """Probe if sort_by is accepted."""
        try:
            data = await client.get("/companies/search", {
                "company_name": "a", "sort_by": "createdon", "sort_order": "asc",
            })
            results = client._extract_results(data)
            assert isinstance(results, list)
        except RecruitCrmError as exc:
            pytest.skip(f"sort_by rejected with {exc.status}")

    async def test_owner_name_filter(self):
        """Probe if owner_name is accepted."""
        try:
            data = await client.get("/companies/search", {"owner_name": "Test"})
            results = client._extract_results(data)
            assert isinstance(results, list)
        except RecruitCrmError as exc:
            pytest.skip(f"owner_name rejected with {exc.status}")

    async def test_owner_email_filter(self):
        """Probe if owner_email is accepted."""
        try:
            data = await client.get("/companies/search", {"owner_email": "test@example.com"})
            results = client._extract_results(data)
            assert isinstance(results, list)
        except RecruitCrmError as exc:
            pytest.skip(f"owner_email rejected with {exc.status}")

    async def test_exact_search_filter(self):
        """Probe if exact_search is accepted."""
        companies = await self._get_companies()
        name = next((c["company_name"] for c in companies if c.get("company_name")), None)
        if not name:
            pytest.skip("No companies with company_name populated")
        try:
            data = await client.get("/companies/search", {
                "company_name": name, "exact_search": "true",
            })
            results = client._extract_results(data)
            assert isinstance(results, list)
        except RecruitCrmError as exc:
            pytest.skip(f"exact_search rejected with {exc.status}")

    async def test_marked_as_off_limit_filter(self):
        """Probe if marked_as_off_limit is accepted."""
        try:
            data = await client.get("/companies/search", {"marked_as_off_limit": "false"})
            results = client._extract_results(data)
            assert isinstance(results, list)
        except RecruitCrmError as exc:
            pytest.skip(f"marked_as_off_limit rejected with {exc.status}")


class TestSearchCompanies:
    """High-level integration tests using client functions."""

    async def test_search_returns_results(self):
        results = await client.search_companies(limit=3)
        assert len(results) > 0

    async def test_results_have_expected_fields(self):
        results = await client.search_companies(limit=1)
        company = results[0]
        assert "slug" in company
        assert "company_name" in company

    async def test_get_company_by_slug(self):
        results = await client.search_companies(limit=1)
        slug = results[0]["slug"]
        company = await client.get_company(slug)
        assert company["slug"] == slug
        assert "company_name" in company

    async def test_summarize_company_from_live_data(self):
        results = await client.search_companies(limit=1)
        summary = CompanySummary.from_api_response(results[0])
        assert summary.slug is not None
        assert summary.company_name


class TestTasks:
    """Raw API probes for tasks endpoints."""

    _cached_tasks: list[dict] | None = None

    async def _get_tasks(self) -> list[dict]:
        if TestTasks._cached_tasks is None:
            data = await client.get("/tasks/search", {"starting_from": "2020-01-01"})
            TestTasks._cached_tasks = client._extract_results(data)
        return TestTasks._cached_tasks

    async def test_search_no_filters_returns_empty(self):
        """/tasks/search with no params returns []."""
        data = await client.get("/tasks/search")
        results = client._extract_results(data)
        assert results == []

    async def test_list_endpoint_exists(self):
        """GET /tasks with limit returns results."""
        data = await client.get("/tasks", {"limit": 3})
        results = client._extract_results(data)
        assert isinstance(results, list)
        assert len(results) > 0

    async def test_task_has_expected_fields(self):
        """Verify field names from a task record.

        Note: tasks use 'id' (integer) not 'slug'.
        """
        tasks = await self._get_tasks()
        if not tasks:
            pytest.skip("No tasks found")
        task = tasks[0]
        for field in [
            "id", "title", "status", "start_date",
            "related_to", "related_to_type", "owner",
        ]:
            assert field in task, f"Expected field {field!r} missing from task"

    async def test_get_task_by_id(self):
        """GET /tasks/{id} returns the matching task."""
        tasks = await self._get_tasks()
        if not tasks:
            pytest.skip("No tasks found")
        task_id = tasks[0]["id"]
        task = await client.get(f"/tasks/{task_id}")
        assert task["id"] == task_id

    async def test_title_filter(self):
        """Discover a title from listing, then filter by it."""
        tasks = await self._get_tasks()
        title = next((t["title"] for t in tasks if t.get("title")), None)
        if not title:
            pytest.skip("No tasks with title populated")

        data = await client.get("/tasks/search", {"title": title})
        results = client._extract_results(data)
        assert len(results) > 0

    async def test_created_from_filter(self):
        """created_from filter should only return tasks created on/after that date."""
        tasks = await self._get_tasks()
        if not tasks or not tasks[0].get("created_on"):
            pytest.skip("No tasks with created_on populated")
        cutoff = tasks[0]["created_on"][:10]
        data = await client.get("/tasks/search", {"created_from": cutoff})
        results = client._extract_results(data)
        if not results:
            pytest.skip("No tasks found matching created_from filter")
        cutoff_dt = datetime.fromisoformat(cutoff).replace(tzinfo=timezone.utc)
        for r in results:
            created_on = r.get("created_on")
            assert created_on, f"Task {r.get('id')} missing created_on"
            dt = _parse_dt(created_on)
            assert dt >= cutoff_dt

    async def test_starting_from_filter(self):
        """starting_from filter should return tasks starting on/after that date."""
        tasks = await self._get_tasks()
        if not tasks or not tasks[0].get("start_date"):
            pytest.skip("No tasks with start_date populated")
        cutoff = tasks[0]["start_date"][:10]
        data = await client.get("/tasks/search", {"starting_from": cutoff})
        results = client._extract_results(data)
        assert len(results) > 0

    async def test_owner_id_filter(self):
        """Discover an owner, filter, verify all results match."""
        tasks = await self._get_tasks()
        owner = next((t["owner"] for t in tasks if t.get("owner")), None)
        if not owner:
            pytest.skip("No tasks with owner populated")

        data = await client.get("/tasks/search", {"owner_id": owner})
        results = client._extract_results(data)
        assert len(results) > 0
        for r in results:
            assert r["owner"] == owner

    async def test_related_to_rejected(self):
        """The API rejects related_to param on /tasks/search with 422."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get("/tasks/search", {"related_to": "test-slug"})
        assert exc_info.value.status == 422

    async def test_related_to_type_rejected(self):
        """The API rejects related_to_type param on /tasks/search with 422."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get("/tasks/search", {"related_to_type": "candidate"})
        assert exc_info.value.status == 422


class TestSearchTasks:
    """High-level integration tests using client functions."""

    async def test_search_returns_results(self):
        results = await client.search_tasks(limit=3)
        assert len(results) > 0

    async def test_results_have_expected_fields(self):
        results = await client.search_tasks(limit=1)
        task = results[0]
        assert "id" in task
        assert "title" in task

    async def test_get_task_by_id(self):
        results = await client.search_tasks(limit=1)
        task_id = results[0]["id"]
        task = await client.get_task(task_id)
        assert task["id"] == task_id
        assert "title" in task

    async def test_summarize_task_from_live_data(self):
        results = await client.search_tasks(limit=1)
        summary = TaskSummary.from_api_response(results[0])
        assert summary.id is not None


class TestNotes:
    """Raw API probes for notes endpoints."""

    _cached_notes: list[dict] | None = None

    async def _get_notes(self) -> list[dict]:
        if TestNotes._cached_notes is None:
            data = await client.get("/notes/search", {"added_from": "2020-01-01"})
            TestNotes._cached_notes = client._extract_results(data)
        return TestNotes._cached_notes

    async def test_search_no_filters_returns_empty(self):
        """/notes/search with no params returns []."""
        data = await client.get("/notes/search")
        results = client._extract_results(data)
        assert results == []

    async def test_list_endpoint_exists(self):
        """GET /notes with limit returns results."""
        data = await client.get("/notes", {"limit": 3})
        results = client._extract_results(data)
        assert isinstance(results, list)
        assert len(results) > 0

    async def test_note_has_expected_fields(self):
        """Verify field names from a note record.

        Note: notes use 'id' (integer) not 'slug'.
        """
        notes = await self._get_notes()
        if not notes:
            pytest.skip("No notes found")
        note = notes[0]
        for field in [
            "id", "note_type", "description",
            "related_to", "related_to_type",
            "created_on", "updated_on",
        ]:
            assert field in note, f"Expected field {field!r} missing from note"

    async def test_get_note_by_id(self):
        """GET /notes/{id} returns the matching note."""
        notes = await self._get_notes()
        if not notes:
            pytest.skip("No notes found")
        note_id = notes[0]["id"]
        note = await client.get(f"/notes/{note_id}")
        assert note["id"] == note_id

    async def test_added_from_filter(self):
        """added_from filter should return notes added on/after that date."""
        notes = await self._get_notes()
        if not notes or not notes[0].get("created_on"):
            pytest.skip("No notes with created_on populated")
        cutoff = notes[0]["created_on"][:10]
        data = await client.get("/notes/search", {"added_from": cutoff})
        results = client._extract_results(data)
        if not results:
            pytest.skip("No notes found matching added_from filter")
        cutoff_dt = datetime.fromisoformat(cutoff).replace(tzinfo=timezone.utc)
        for r in results:
            created_on = r.get("created_on")
            assert created_on, f"Note {r.get('id')} missing created_on"
            dt = _parse_dt(created_on)
            assert dt >= cutoff_dt

    async def test_related_to_rejected(self):
        """The API rejects related_to param on /notes/search with 422."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get("/notes/search", {"related_to": "test-slug"})
        assert exc_info.value.status == 422

    async def test_related_to_type_rejected(self):
        """The API rejects related_to_type param on /notes/search with 422."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get("/notes/search", {"related_to_type": "candidate"})
        assert exc_info.value.status == 422

    async def test_created_from_rejected(self):
        """The API rejects created_from param (uses added_from instead) with 400."""
        with pytest.raises(RecruitCrmError) as exc_info:
            await client.get("/notes/search", {"created_from": "2020-01-01"})
        assert exc_info.value.status == 400


class TestSearchNotes:
    """High-level integration tests using client functions."""

    async def test_search_returns_results(self):
        results = await client.search_notes(limit=3)
        assert len(results) > 0

    async def test_results_have_expected_fields(self):
        results = await client.search_notes(limit=1)
        note = results[0]
        assert "id" in note
        assert "note_type" in note

    async def test_get_note_by_id(self):
        results = await client.search_notes(limit=1)
        note_id = results[0]["id"]
        note = await client.get_note(note_id)
        assert note["id"] == note_id

    async def test_summarize_note_from_live_data(self):
        results = await client.search_notes(limit=1)
        summary = NoteSummary.from_api_response(results[0])
        assert summary.id is not None


class TestLookups:
    """Integration tests for the 11 lookup endpoints."""

    async def test_list_note_types(self):
        results = await client.list_note_types()
        assert isinstance(results, list)
        if results:
            item = results[0]
            assert item.get("id") is not None
            assert item.get("label")
            LookupItem.from_api_response(item)  # validates shape

    async def test_list_meeting_types(self):
        results = await client.list_meeting_types()
        assert isinstance(results, list)
        if results:
            item = results[0]
            assert item.get("id") is not None
            assert item.get("label")
            LookupItem.from_api_response(item)

    async def test_list_task_types(self):
        results = await client.list_task_types()
        assert isinstance(results, list)
        if results:
            item = results[0]
            assert item.get("id") is not None
            assert item.get("label")
            LookupItem.from_api_response(item)

    async def test_list_hiring_pipelines(self):
        results = await client.list_hiring_pipelines()
        assert isinstance(results, list)
        # Master pipeline (id=0) is always present on every tenant
        assert len(results) > 0
        item = results[0]
        assert item.get("id") is not None
        assert item.get("label")
        LookupItem.from_api_response(item)

    async def test_list_hiring_pipeline_stages_master(self):
        """Master pipeline (id=0) should always return at least some stages."""
        results = await client.list_hiring_pipeline_stages(0)
        assert isinstance(results, list)
        if results:
            item = results[0]
            assert item.get("id") is not None
            assert item.get("label")
            LookupItem.from_api_response(item)

    async def test_list_contact_stages(self):
        results = await client.list_contact_stages()
        assert isinstance(results, list)
        if results:
            item = results[0]
            assert item.get("id") is not None
            assert item.get("label")
            LookupItem.from_api_response(item)

    async def test_list_industries(self):
        results = await client.list_industries()
        assert isinstance(results, list)
        # Industries list is a Recruit CRM platform default — always non-empty
        assert len(results) > 0
        item = results[0]
        assert item.get("id") is not None
        assert item.get("label")
        LookupItem.from_api_response(item)

    async def test_list_company_custom_fields(self):
        results = await client.list_company_custom_fields()
        assert isinstance(results, list)
        if results:
            item = results[0]
            assert item.get("id") is not None
            assert item.get("label")
            # field_type should be preserved from the API response
            assert "field_type" in item
            LookupItem.from_api_response(item)

    async def test_list_contact_custom_fields(self):
        results = await client.list_contact_custom_fields()
        assert isinstance(results, list)
        if results:
            item = results[0]
            assert item.get("id") is not None
            assert item.get("label")
            assert "field_type" in item
            LookupItem.from_api_response(item)

    async def test_list_job_custom_fields(self):
        results = await client.list_job_custom_fields()
        assert isinstance(results, list)
        if results:
            item = results[0]
            assert item.get("id") is not None
            assert item.get("label")
            assert "field_type" in item
            LookupItem.from_api_response(item)

    async def test_list_candidate_custom_fields(self):
        results = await client.list_candidate_custom_fields()
        assert isinstance(results, list)
        if results:
            item = results[0]
            assert item.get("id") is not None
            assert item.get("label")
            assert "field_type" in item
            LookupItem.from_api_response(item)


class TestWrites:
    """Integration tests for the four PR 1 write tools.

    Anchors use throwaway fixture entities (see tests/integration/conftest.py)
    so writes never touch real tenant records. Each test also deletes its own
    note/task/meeting in a try/finally.
    """

    async def test_create_note_round_trip(self, test_candidate):
        description = _test_label("Note")
        payload = {
            "description": description,
            "related_to": test_candidate,
            "related_to_type": "candidate",
        }
        created = await client.create_note(payload)
        note_id = created.get("id")
        assert note_id, f"Expected id in create-note response, got {created!r}"
        try:
            fetched = await client.get_note(note_id)
            assert fetched["id"] == note_id
            assert fetched.get("description") == description
            assert fetched.get("related_to") == test_candidate
            assert fetched.get("related_to_type") == "candidate"
        finally:
            await client.delete(f"/notes/{note_id}")

    async def test_create_task_round_trip_and_update(self, test_candidate):
        title = _test_label("Task")
        payload = {
            "title": title,
            "start_date": "2030-01-01T09:00:00Z",
            "reminder": -1,
            "related_to": test_candidate,
            "related_to_type": "candidate",
        }
        created = await client.create_task(payload)
        task_id = created.get("id")
        assert task_id, f"Expected id in create-task response, got {created!r}"
        try:
            fetched = await client.get_task(task_id)
            assert fetched["id"] == task_id
            assert fetched.get("title") == title

            # update_task round-trip — change the description
            updated = await client.update_task(task_id, {"description": "updated"})
            assert updated.get("id") == task_id
            fetched = await client.get_task(task_id)
            assert fetched.get("description") == "updated"
        finally:
            await client.delete(f"/tasks/{task_id}")

    async def test_update_task_preserves_omitted_fields(self, test_candidate):
        """Partial update should preserve fields not in the patch.

        Creates a task with 5 fields, updates only ``description``, asserts all
        other fields survive. Per edit-task.md every body field is optional, so
        the API is expected to support true partial updates.
        """
        title = _test_label("PreserveTask")
        payload = {
            "title": title,
            "description": "original description",
            "start_date": "2030-01-01T09:00:00Z",
            "reminder": 1440,
            "related_to": test_candidate,
            "related_to_type": "candidate",
        }
        created = await client.create_task(payload)
        task_id = created.get("id")
        assert task_id, f"create failed: {created!r}"
        try:
            await client.update_task(task_id, {"description": "patched description"})
            fetched = await client.get_task(task_id)
            assert fetched.get("description") == "patched description", (
                f"description not updated: {fetched.get('description')!r}"
            )
            assert fetched.get("title") == title, (
                f"title not preserved: {fetched.get('title')!r}"
            )
            assert fetched.get("related_to") == test_candidate, (
                f"related_to not preserved: {fetched.get('related_to')!r}"
            )
            assert fetched.get("related_to_type") == "candidate", (
                f"related_to_type not preserved: {fetched.get('related_to_type')!r}"
            )
            assert fetched.get("reminder") == 1440, (
                f"reminder not preserved: {fetched.get('reminder')!r}"
            )
        finally:
            await client.delete(f"/tasks/{task_id}")

    async def test_log_meeting_round_trip(self, test_candidate):
        # No attendees/users — belt-and-suspenders for the "no invites" guarantee,
        # even if do_not_send_calendar_invites is misinterpreted by the API.
        title = _test_label("Meeting")
        payload = {
            "title": title,
            "start_date": "2030-01-01T09:00:00Z",
            "end_date": "2030-01-01T10:00:00Z",
            "reminder": -1,
            "related_to": test_candidate,
            "related_to_type": "candidate",
            "do_not_send_calendar_invites": True,
        }
        created = await client.create_meeting(payload)
        meeting_id = created.get("id")
        assert meeting_id, f"Expected id in create-meeting response, got {created!r}"
        try:
            fetched = await client.get_meeting(meeting_id)
            assert fetched["id"] == meeting_id
            assert fetched.get("title") == title
            # API may serialize this as bool, int, or string — accept any truthy form.
            flag = fetched.get("do_not_send_calendar_invites")
            assert flag in (True, 1, "1", "true"), (
                f"Expected do_not_send_calendar_invites truthy, got {flag!r}"
            )
        finally:
            await client.delete(f"/meetings/{meeting_id}")


def _ts() -> str:
    """Return a compact UTC timestamp (with microseconds) for unique test-entity suffixes.

    Microsecond precision avoids collisions when tests retry within the same
    second (second-level resolution caused flakes under concurrent / retried runs).
    """
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")


class TestWriteSurface:
    """Integration tests for the Avery Knapp write-surface (CRUD + assignment + upload).

    Every test cleans up via try/finally. The tests hit the live Recruit CRM
    tenant — stray records are a real problem.
    """

    async def test_create_update_company_round_trip(self):
        created = await client.create_company({
            "company_name": _test_label("CompanyRT"),
            "about_company": "x",
            "website": "https://example.invalid",
        })
        slug = created.get("slug")
        assert slug, f"Expected slug in create-company response, got {created!r}"
        try:
            updated = await client.update_company(slug, {"about_company": "y"})
            assert updated.get("slug") == slug
            fetched = await client.get_company(slug)
            assert fetched.get("slug") == slug
            assert fetched.get("about_company") == "y"
        finally:
            await client.delete(f"/companies/{slug}")

    async def test_create_update_contact_round_trip(self):
        first_name = _test_label("ContactRT")
        created = await client.create_contact({
            "first_name": first_name,
            "last_name": "Fixture",
            "email": f"{first_name.lower()}@example.invalid",
        })
        slug = created.get("slug")
        assert slug, f"Expected slug in create-contact response, got {created!r}"
        try:
            new_designation = "Updated by MCP test"
            updated = await client.update_contact(slug, {"designation": new_designation})
            assert updated.get("slug") == slug
            fetched = await client.get_contact(slug)
            assert fetched.get("slug") == slug
            assert fetched.get("designation") == new_designation
        finally:
            await client.delete(f"/contacts/{slug}")

    async def test_create_update_job_round_trip(self):
        company_resp = await client.create_company({"company_name": _test_label("JobRTCo")})
        company_slug = company_resp.get("slug")
        assert company_slug, f"Expected company slug, got {company_resp!r}"
        try:
            contact_resp = await client.create_contact({
                "first_name": _test_label("JobRTContact"),
                "last_name": "Fixture",
                "company_slug": company_slug,
            })
            contact_slug = contact_resp.get("slug")
            assert contact_slug, f"Expected contact slug, got {contact_resp!r}"
            try:
                job_resp = await client.create_job({
                    "name": _test_label("JobRT"),
                    "company_slug": company_slug,
                    "contact_slug": contact_slug,
                    "number_of_openings": 1,
                    "currency_id": 1,
                    "enable_job_application_form": 0,
                    "job_description_text": "Test job",
                })
                job_slug = job_resp.get("slug")
                assert job_slug, f"Expected job slug, got {job_resp!r}"
                try:
                    updated = await client.update_job(
                        job_slug, {"note_for_candidates": "updated"}
                    )
                    assert updated.get("slug") == job_slug
                    fetched = await client.get_job(job_slug)
                    assert fetched.get("slug") == job_slug
                    assert fetched.get("note_for_candidates") == "updated"
                finally:
                    await client.delete(f"/jobs/{job_slug}")
            finally:
                await client.delete(f"/contacts/{contact_slug}")
        finally:
            await client.delete(f"/companies/{company_slug}")

    async def test_create_update_candidate_round_trip(self):
        first_name = _test_label("CandidateRT")
        created = await client.create_candidate({
            "first_name": first_name,
            "last_name": "Fixture",
            "email": f"{first_name.lower()}@example.invalid",
        })
        slug = created.get("slug")
        assert slug, f"Expected slug in create-candidate response, got {created!r}"
        try:
            updated = await client.update_candidate(slug, {"position": "Updated by MCP"})
            assert updated.get("slug") == slug
            fetched = await client.get_candidate(slug)
            assert fetched.get("slug") == slug
            assert fetched.get("position") == "Updated by MCP"
        finally:
            await client.delete(f"/candidates/{slug}")

    async def test_update_meeting_round_trip(self, test_candidate):
        from recruit_crm_mcp.models import EntityRef
        from recruit_crm_mcp.server import log_meeting, update_meeting

        original_title = _test_label("MeetingRT")
        new_title = f"{original_title} (updated)"
        created = await log_meeting(
            title=original_title,
            start_date="2030-01-01T09:00:00Z",
            end_date="2030-01-01T10:00:00Z",
            related_to=EntityRef(kind="candidate", id=test_candidate),
            reminder=-1,
            do_not_send_calendar_invites=True,
        )
        meeting_id = int(created.id) if created.id else None
        assert meeting_id, f"Expected meeting id, got {created!r}"
        try:
            result = await update_meeting(meeting_id=meeting_id, title=new_title)
            assert result.kind == "meeting"
            fetched = await client.get_meeting(meeting_id)
            assert fetched["id"] == meeting_id
            assert fetched.get("title") == new_title
        finally:
            await client.delete(f"/meetings/{meeting_id}")

    async def test_delete_note_removes_note(self, test_candidate):
        payload = {
            "description": _test_label("DeleteNote"),
            "related_to": test_candidate,
            "related_to_type": "candidate",
        }
        created = await client.create_note(payload)
        note_id = created.get("id")
        assert note_id, f"Expected id in create-note response, got {created!r}"
        deleted = False
        try:
            await client.delete_note(note_id)
            deleted = True
            with pytest.raises(RecruitCrmError) as exc_info:
                await client.get_note(note_id)
            assert exc_info.value.status == 404
        finally:
            if not deleted:
                # Belt-and-suspenders: if delete_note raised, ensure cleanup.
                try:
                    await client.delete(f"/notes/{note_id}")
                except Exception:
                    pass


class TestCustomFieldsWrites:
    """Round-trip tests for set_*_custom_fields tools.

    Each test skips when the tenant has no custom fields of the relevant type,
    since we can't round-trip a value without a live field_id.
    """

    @staticmethod
    def _find_value(custom_fields: list[dict] | None, field_id: int) -> str | None:
        """Pick the value for a specific field_id out of a custom_fields array."""
        if not custom_fields:
            return None
        for cf in custom_fields:
            if cf.get("field_id") == field_id:
                return cf.get("value")
        return None

    async def test_set_company_custom_fields(self):
        from recruit_crm_mcp.models import CustomFieldValue
        from recruit_crm_mcp.server import set_company_custom_fields

        fields = await client.list_company_custom_fields()
        if not fields:
            pytest.skip("Tenant has no company custom fields")
        field_id = fields[0]["id"]

        company = await client.create_company({"company_name": _test_label("CFCo")})
        slug = company.get("slug")
        assert slug, f"Expected slug, got {company!r}"
        try:
            test_value = _test_label("CFVal")
            result = await set_company_custom_fields(
                slug=slug,
                fields=[CustomFieldValue(field_id=field_id, value=test_value)],
            )
            assert result.kind == "company"
            fetched = await client.get_company(slug)
            got = self._find_value(fetched.get("custom_fields"), field_id)
            assert got == test_value, (
                f"Expected custom field {field_id}={test_value!r}, got {got!r}"
            )
        finally:
            await client.delete(f"/companies/{slug}")

    async def test_set_contact_custom_fields(self):
        from recruit_crm_mcp.models import CustomFieldValue
        from recruit_crm_mcp.server import set_contact_custom_fields

        fields = await client.list_contact_custom_fields()
        if not fields:
            pytest.skip("Tenant has no contact custom fields")
        field_id = fields[0]["id"]

        first_name = _test_label("CFContact")
        contact = await client.create_contact({
            "first_name": first_name,
            "last_name": "Fixture",
            "email": f"{first_name.lower()}@example.invalid",
        })
        slug = contact.get("slug")
        assert slug, f"Expected slug, got {contact!r}"
        try:
            test_value = _test_label("CFVal")
            result = await set_contact_custom_fields(
                slug=slug,
                fields=[CustomFieldValue(field_id=field_id, value=test_value)],
            )
            assert result.kind == "contact"
            fetched = await client.get_contact(slug)
            got = self._find_value(fetched.get("custom_fields"), field_id)
            assert got == test_value, (
                f"Expected custom field {field_id}={test_value!r}, got {got!r}"
            )
        finally:
            await client.delete(f"/contacts/{slug}")

    async def test_set_job_custom_fields(self):
        from recruit_crm_mcp.models import CustomFieldValue
        from recruit_crm_mcp.server import set_job_custom_fields

        fields = await client.list_job_custom_fields()
        if not fields:
            pytest.skip("Tenant has no job custom fields")
        field_id = fields[0]["id"]

        # Job requires company + contact; build throwaway anchors.
        company = await client.create_company({"company_name": _test_label("CFJobCo")})
        company_slug = company.get("slug")
        assert company_slug, f"Expected company slug, got {company!r}"
        try:
            contact = await client.create_contact({
                "first_name": _test_label("CFJobContact"),
                "last_name": "Fixture",
                "company_slug": company_slug,
            })
            contact_slug = contact.get("slug")
            assert contact_slug, f"Expected contact slug, got {contact!r}"
            try:
                job = await client.create_job({
                    "name": _test_label("CFJob"),
                    "company_slug": company_slug,
                    "contact_slug": contact_slug,
                    "number_of_openings": 1,
                    "currency_id": 1,
                    "enable_job_application_form": 0,
                    "job_description_text": "CF job",
                })
                job_slug = job.get("slug")
                assert job_slug, f"Expected job slug, got {job!r}"
                try:
                    test_value = _test_label("CFVal")
                    result = await set_job_custom_fields(
                        slug=job_slug,
                        fields=[CustomFieldValue(field_id=field_id, value=test_value)],
                    )
                    assert result.kind == "job"
                    fetched = await client.get_job(job_slug)
                    got = self._find_value(fetched.get("custom_fields"), field_id)
                    assert got == test_value, (
                        f"Expected custom field {field_id}={test_value!r}, got {got!r}"
                    )
                finally:
                    await client.delete(f"/jobs/{job_slug}")
            finally:
                await client.delete(f"/contacts/{contact_slug}")
        finally:
            await client.delete(f"/companies/{company_slug}")

    async def test_set_candidate_custom_fields(self):
        from recruit_crm_mcp.models import CustomFieldValue
        from recruit_crm_mcp.server import set_candidate_custom_fields

        fields = await client.list_candidate_custom_fields()
        if not fields:
            pytest.skip("Tenant has no candidate custom fields")
        field_id = fields[0]["id"]

        first_name = _test_label("CFCand")
        candidate = await client.create_candidate({
            "first_name": first_name,
            "last_name": "Fixture",
            "email": f"{first_name.lower()}@example.invalid",
        })
        slug = candidate.get("slug")
        assert slug, f"Expected slug, got {candidate!r}"
        try:
            test_value = _test_label("CFVal")
            result = await set_candidate_custom_fields(
                slug=slug,
                fields=[CustomFieldValue(field_id=field_id, value=test_value)],
            )
            assert result.kind == "candidate"
            fetched = await client.get_candidate(slug)
            got = self._find_value(fetched.get("custom_fields"), field_id)
            assert got == test_value, (
                f"Expected custom field {field_id}={test_value!r}, got {got!r}"
            )
        finally:
            await client.delete(f"/candidates/{slug}")


class TestAssignmentWrites:
    """Integration tests for the assignment trio: assign / unassign / update_hiring_stage."""

    async def test_assign_and_unassign_candidate(self, test_candidate):
        # Build a throwaway company + contact + job to avoid polluting real records.
        company = await client.create_company({"company_name": _test_label("AssignCo")})
        company_slug = company.get("slug")
        assert company_slug, f"Expected company slug, got {company!r}"
        try:
            contact = await client.create_contact({
                "first_name": _test_label("AssignContact"),
                "last_name": "Fixture",
                "company_slug": company_slug,
            })
            contact_slug = contact.get("slug")
            assert contact_slug, f"Expected contact slug, got {contact!r}"
            try:
                job = await client.create_job({
                    "name": _test_label("AssignJob"),
                    "company_slug": company_slug,
                    "contact_slug": contact_slug,
                    "number_of_openings": 1,
                    "currency_id": 1,
                    "enable_job_application_form": 0,
                    "job_description_text": "Assign job",
                })
                job_slug = job.get("slug")
                assert job_slug, f"Expected job slug, got {job!r}"
                try:
                    assign_resp = await client.assign_candidate(test_candidate, job_slug)
                    # Response should echo our candidate slug.
                    assert assign_resp.get("candidate_slug") == test_candidate
                    unassigned = False
                    try:
                        # Confirm the assignment is visible on the job.
                        assigned = await client.get_assigned_candidates(job_slug)
                        assert any(
                            (item.get("candidate") or {}).get("slug") == test_candidate
                            for item in assigned
                        ), f"Expected {test_candidate} in assigned list, got {assigned!r}"
                    finally:
                        await client.unassign_candidate(test_candidate, job_slug)
                        unassigned = True
                    assert unassigned
                finally:
                    await client.delete(f"/jobs/{job_slug}")
            finally:
                await client.delete(f"/contacts/{contact_slug}")
        finally:
            await client.delete(f"/companies/{company_slug}")

    async def test_update_hiring_stage(self, test_candidate):
        stages = await client.list_hiring_pipeline_stages(0)
        if not stages:
            pytest.skip("Tenant has no master hiring-pipeline stages")
        status_id = stages[0]["id"]
        if status_id is None:
            pytest.skip("Master pipeline stage lacks an id")

        company = await client.create_company({"company_name": _test_label("StageCo")})
        company_slug = company.get("slug")
        assert company_slug, f"Expected company slug, got {company!r}"
        try:
            contact = await client.create_contact({
                "first_name": _test_label("StageContact"),
                "last_name": "Fixture",
                "company_slug": company_slug,
            })
            contact_slug = contact.get("slug")
            assert contact_slug, f"Expected contact slug, got {contact!r}"
            try:
                job = await client.create_job({
                    "name": _test_label("StageJob"),
                    "company_slug": company_slug,
                    "contact_slug": contact_slug,
                    "number_of_openings": 1,
                    "currency_id": 1,
                    "enable_job_application_form": 0,
                    "job_description_text": "Stage job",
                })
                job_slug = job.get("slug")
                assert job_slug, f"Expected job slug, got {job!r}"
                try:
                    await client.assign_candidate(test_candidate, job_slug)
                    try:
                        resp = await client.update_hiring_stage(
                            test_candidate, job_slug, {"status_id": status_id}
                        )
                        # Either the response echoes a candidate_slug or it silently
                        # succeeds with an empty body — both are acceptable.
                        echoed = resp.get("candidate_slug")
                        assert echoed in (test_candidate, None), (
                            f"Unexpected candidate_slug in response: {echoed!r}"
                        )
                    finally:
                        await client.unassign_candidate(test_candidate, job_slug)
                finally:
                    await client.delete(f"/jobs/{job_slug}")
            finally:
                await client.delete(f"/contacts/{contact_slug}")
        finally:
            await client.delete(f"/companies/{company_slug}")


class TestFileUploadWrites:
    """Integration tests for file upload.

    Recruit CRM has no public DELETE /files endpoint — the uploaded file will
    leak by design. We anchor the upload to a throwaway candidate and delete
    the candidate, which implicitly orphans the file. Folder names include a
    timestamp suffix so reruns don't collide in the UI.
    """

    async def test_upload_file_url(self, test_candidate):
        ts = _ts()
        # Small public PNG — GNU GPLv3 badge is stable and light.
        file_url = "https://www.gnu.org/graphics/gplv3-127x51.png"
        folder = f"mcp-test-{ts}"
        resp = await client.upload_file(
            file_url=file_url,
            related_to=test_candidate,
            related_to_type="candidate",
            folder=folder,
        )
        # Response should carry at least a file_link for the uploaded asset.
        assert resp.get("file_link"), (
            f"Expected file_link in upload response, got {resp!r}"
        )
