"""Integration tests against the live Recruit CRM API.

Requires RECRUIT_CRM_API_KEY in environment (loaded from .env via pytest-dotenv).
Run with: make integration-test
"""

import os

import pytest

from recruit_crm_mcp import client
from recruit_crm_mcp.server import _summarize_candidate, _summarize_job

pytestmark = [
    pytest.mark.anyio,
    pytest.mark.integration,
    pytest.mark.skipif(
        not os.environ.get("RECRUIT_CRM_API_KEY"),
        reason="RECRUIT_CRM_API_KEY not set",
    ),
]


class TestFindCandidates:
    async def test_list_returns_results(self):
        results = await client.find_candidates(limit=3)
        assert len(results) > 0

    async def test_list_results_have_expected_fields(self):
        results = await client.find_candidates(limit=1)
        candidate = results[0]
        assert "slug" in candidate
        assert "first_name" in candidate
        assert "last_name" in candidate
        assert "position" in candidate
        assert "current_organization" in candidate

    async def test_list_enforces_limit(self):
        results = await client.find_candidates(limit=3)
        assert len(results) <= 3

    async def test_summarize_candidate_from_live_data(self):
        results = await client.find_candidates(limit=1)
        summary = _summarize_candidate(results[0])
        assert summary["slug"] is not None
        assert summary["name"]  # non-empty

    async def test_get_candidate_by_slug(self):
        results = await client.find_candidates(limit=1)
        slug = results[0]["slug"]
        candidate = await client.get_candidate(slug)
        assert candidate["slug"] == slug
        assert "first_name" in candidate

    async def test_candidate_resume_field_structure(self):
        results = await client.find_candidates(limit=5)
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

    async def test_search_with_first_name_returns_matches(self):
        """Regression for MAIN-85: search filters were silently ignored."""
        baseline = await client.find_candidates(limit=1)
        assert len(baseline) > 0
        target_name = baseline[0].get("first_name")
        if not target_name:
            pytest.skip("First candidate has no first_name")

        filtered = await client.find_candidates(
            first_name=target_name, limit=25
        )
        assert len(filtered) > 0
        # API uses like-matching, so "Kelly" may match "Kellyn"
        for c in filtered:
            assert target_name.lower() in c["first_name"].lower(), (
                f"Expected first_name containing {target_name!r}, "
                f"got {c['first_name']!r}"
            )

    async def test_search_with_email_returns_specific_candidate(self):
        baseline = await client.find_candidates(limit=1)
        assert len(baseline) > 0
        target_email = baseline[0].get("email")
        if not target_email:
            pytest.skip("First candidate has no email")

        filtered = await client.find_candidates(email=target_email, limit=10)
        assert len(filtered) >= 1
        emails = [c.get("email", "").lower() for c in filtered]
        assert target_email.lower() in emails

    async def test_different_filters_return_different_results(self):
        """Core MAIN-85 regression: different filters must NOT return
        identical result sets."""
        results_a = await client.find_candidates(country="US", limit=10)
        results_b = await client.find_candidates(country="India", limit=10)

        if results_a and results_b:
            slugs_a = {c["slug"] for c in results_a}
            slugs_b = {c["slug"] for c in results_b}
            assert slugs_a != slugs_b, (
                "Different country filters returned identical results — "
                "filters are likely being ignored"
            )


class TestJobs:
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
