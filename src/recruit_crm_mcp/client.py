"""HTTP client for the Recruit CRM API."""

import os
from typing import Any

import httpx

API_BASE = "https://api.recruitcrm.io/v1"


def _get_api_key() -> str:
    key = os.environ.get("RECRUIT_CRM_API_KEY")
    if not key:
        raise RuntimeError("RECRUIT_CRM_API_KEY environment variable is required")
    return key


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_get_api_key()}",
        "Accept": "application/json",
    }


async def get(path: str, params: dict[str, Any] | None = None) -> dict:
    """Make a GET request to the Recruit CRM API."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{API_BASE}{path}",
            headers=_headers(),
            params=params,
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()


async def search_candidates(
    query: str | None = None,
    email: str | None = None,
    city: str | None = None,
    job_title: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """Search for candidates using available filters."""
    params: dict[str, Any] = {"per_page": limit}
    if email:
        params["email"] = email
    if city:
        params["city"] = city
    if job_title:
        params["job_title"] = job_title

    # Use search endpoint for free-text queries, list endpoint for field filters
    if query and not any([email, city, job_title]):
        params["search"] = query
        data = await get("/candidates/search", params)
    else:
        data = await get("/candidates", params)

    # API returns paginated response with "data" key
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    if isinstance(data, list):
        return data
    return [data] if data else []


async def get_candidate(candidate_slug: str) -> dict:
    """Get a single candidate by slug/ID."""
    return await get(f"/candidates/{candidate_slug}")


async def list_jobs(status: str | None = None, limit: int = 20) -> list[dict]:
    """List jobs, optionally filtered by status."""
    params: dict[str, Any] = {"per_page": limit}
    if status:
        params["status"] = status
    data = await get("/jobs", params)
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    if isinstance(data, list):
        return data
    return [data] if data else []


async def get_job(job_slug: str) -> dict:
    """Get a single job by slug/ID."""
    return await get(f"/jobs/{job_slug}")
