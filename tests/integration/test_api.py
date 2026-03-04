"""Integration tests against the live Recruit CRM API.

Requires RECRUIT_CRM_API_KEY in environment (loaded from .env via pytest-dotenv).
Run with: make integration-test
"""

import os
from datetime import datetime, timezone

import httpx
import pytest

from recruit_crm_mcp import client
from recruit_crm_mcp.server import (
    _summarize_candidate,
    _summarize_company,
    _summarize_contact,
    _summarize_job,
    _summarize_meeting,
    _summarize_user,
)


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
        summary = _summarize_candidate(results[0])
        assert summary["slug"] is not None
        assert summary["name"]  # non-empty

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
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await client.get(
                "/candidates/search",
                {"country": "United States", "sort_by": "updated_at"},
            )
        assert exc_info.value.response.status_code == 422

    async def test_sort_by_rejected_on_list_endpoint(self):
        """The API rejects sort_by/sort_order on /candidates with 422."""
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await client.get(
                "/candidates",
                {"limit": 1, "sort_by": "updated_at", "sort_order": "desc"},
            )
        assert exc_info.value.response.status_code == 422

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
        summary = _summarize_job(results[0])
        assert summary["slug"] is not None
        assert summary["name"]
        assert summary["status"]  # should resolve from job_status.label

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
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await client.get("/jobs/search", {"created_on": "2025-01-01"})
        assert exc_info.value.response.status_code == 400

    async def test_updated_on_rejected(self):
        """The API rejects updated_on param with 400."""
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await client.get("/jobs/search", {"updated_on": "2025-01-01"})
        assert exc_info.value.response.status_code == 400

    async def test_owner_rejected(self):
        """The API rejects owner param (not owner_id) with 400."""
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await client.get("/jobs/search", {"owner": 1})
        assert exc_info.value.response.status_code == 400


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
        summary = _summarize_user(results[0])
        assert summary["id"] is not None
        assert summary["name"]
        # email may be None for some users
        assert "email" in summary


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
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await client.get("/contacts/search", {"designation": "VP Sales"})
        assert exc_info.value.response.status_code == 400


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
        summary = _summarize_contact(results[0])
        assert summary["slug"] is not None
        assert summary["name"]


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
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await client.get("/meetings/search", {"related_to": "test-slug"})
        assert exc_info.value.response.status_code == 422

    async def test_related_to_type_rejected(self):
        """The API rejects related_to_type param on /meetings/search with 422."""
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await client.get("/meetings/search", {"related_to_type": "candidate"})
        assert exc_info.value.response.status_code == 422


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
        summary = _summarize_meeting(results[0])
        assert summary["id"] is not None
        assert summary["title"]


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
        except httpx.HTTPStatusError as exc:
            pytest.skip(f"sort_by rejected with {exc.response.status_code}")

    async def test_owner_name_filter(self):
        """Probe if owner_name is accepted."""
        try:
            data = await client.get("/companies/search", {"owner_name": "Test"})
            results = client._extract_results(data)
            assert isinstance(results, list)
        except httpx.HTTPStatusError as exc:
            pytest.skip(f"owner_name rejected with {exc.response.status_code}")

    async def test_owner_email_filter(self):
        """Probe if owner_email is accepted."""
        try:
            data = await client.get("/companies/search", {"owner_email": "test@example.com"})
            results = client._extract_results(data)
            assert isinstance(results, list)
        except httpx.HTTPStatusError as exc:
            pytest.skip(f"owner_email rejected with {exc.response.status_code}")

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
        except httpx.HTTPStatusError as exc:
            pytest.skip(f"exact_search rejected with {exc.response.status_code}")

    async def test_marked_as_off_limit_filter(self):
        """Probe if marked_as_off_limit is accepted."""
        try:
            data = await client.get("/companies/search", {"marked_as_off_limit": "false"})
            results = client._extract_results(data)
            assert isinstance(results, list)
        except httpx.HTTPStatusError as exc:
            pytest.skip(f"marked_as_off_limit rejected with {exc.response.status_code}")


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
        summary = _summarize_company(results[0])
        assert summary["slug"] is not None
        assert summary["company_name"]
