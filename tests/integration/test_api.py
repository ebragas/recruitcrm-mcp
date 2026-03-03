"""Integration tests against the live Recruit CRM API.

Requires RECRUIT_CRM_API_KEY in environment (loaded from .env via pytest-dotenv).
Run with: make integration-test
"""

import os
from datetime import datetime, timezone

import httpx
import pytest

from recruit_crm_mcp import client
from recruit_crm_mcp.server import _summarize_candidate, _summarize_job


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
