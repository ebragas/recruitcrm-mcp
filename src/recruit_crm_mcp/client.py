"""HTTP client for the Recruit CRM API."""

import asyncio
import logging
import os
import time
from typing import Any

import httpx

logger = logging.getLogger(__name__)

API_BASE = "https://api.recruitcrm.io/v1"

_client: httpx.AsyncClient | None = None


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


async def _get_client() -> httpx.AsyncClient:
    """Get a shared AsyncClient instance for connection pooling."""
    global _client
    if _client is None:
        _client = httpx.AsyncClient()
    return _client


async def aclose_client() -> None:
    """Close the shared AsyncClient. Call on application shutdown."""
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


def _parse_retry_after(resp: httpx.Response) -> float:
    """Extract wait time from rate limit response headers.

    Checks Retry-After first, then falls back to X-RateLimit headers.
    Returns a default of 10 seconds if no usable header is found.
    """
    retry_after = resp.headers.get("Retry-After")
    if retry_after:
        try:
            wait = float(retry_after)
            if wait > 0:
                return min(wait, 120.0)
        except ValueError:
            pass

    # Some APIs provide a reset timestamp (seconds since epoch)
    reset = resp.headers.get("X-RateLimit-Reset")
    if reset:
        try:
            wait = float(reset) - time.time()
            if wait > 0:
                return min(wait, 120.0)
        except ValueError:
            pass

    return 10.0


async def get(path: str, params: dict[str, Any] | None = None) -> Any:
    """Make a GET request to the Recruit CRM API.

    Retries once on 429 (rate limited) after waiting for the duration
    indicated by the response headers.
    """
    client = await _get_client()
    url = f"{API_BASE}{path}"
    kwargs = {"headers": _headers(), "params": params, "timeout": 30.0}

    resp = await client.get(url, **kwargs)

    if resp.status_code == 429:
        wait = _parse_retry_after(resp)
        logger.warning("Rate limited on %s — retrying in %.1fs", path, wait)
        await asyncio.sleep(wait)
        resp = await client.get(url, **kwargs)

    resp.raise_for_status()
    return resp.json()


async def search_candidates(
    query: str | None = None,
    email: str | None = None,
    city: str | None = None,
    job_title: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """Search for candidates using available filters.

    Note: ``query`` (free-text search) and field filters (email, city,
    job_title) are mutually exclusive.  When any field filter is provided,
    ``query`` is ignored and the list endpoint with field filters is used
    instead of the search endpoint.
    """
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
        results = data["data"]
    elif isinstance(data, list):
        results = data
    else:
        results = [data] if data else []

    # API ignores per_page below its minimum (100), so enforce limit client-side
    return results[:limit]


async def get_candidate(candidate_slug: str) -> dict:
    """Get a single candidate by slug/ID."""
    return await get(f"/candidates/{candidate_slug}")


# Maps user-facing status labels → API integer IDs for /jobs/search.
# Note: "Closed" has ID 0, which the API treats as no filter (returns []).
# Closed jobs cannot be filtered via /jobs/search.
JOB_STATUS_IDS: dict[str, int] = {
    "open": 1,
    "on hold": 2,
    "canceled": 3,
    "closed": 0,
    "placed": 1004,
    "refill": 1406,
}


async def list_jobs(limit: int = 20) -> list[dict]:
    """List jobs via the /jobs endpoint (no filtering).

    The API always returns at least 15 per page; ``limit`` is enforced
    client-side.
    """
    data = await get("/jobs", {"per_page": limit})

    if isinstance(data, dict) and "data" in data:
        results = data["data"]
    elif isinstance(data, list):
        results = data
    else:
        results = [data] if data else []

    return results[:limit]


async def search_jobs(
    status: str | None = None,
    name: str | None = None,
    city: str | None = None,
    country: str | None = None,
    company_name: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """Search for jobs via the /jobs/search endpoint.

    At least one filter must be provided — the API returns an empty list
    when called with no filters.

    ``status`` accepts a label string (e.g. 'Open', 'Closed') which is
    mapped to the integer ID the API expects.
    """
    params: dict[str, Any] = {}
    if status:
        status_id = JOB_STATUS_IDS.get(status.lower())
        if status_id is None:
            valid = ", ".join(sorted(JOB_STATUS_IDS.keys(), key=lambda k: JOB_STATUS_IDS[k]))
            raise ValueError(
                f"Unknown job status {status!r}. Valid values: {valid}"
            )
        params["job_status"] = status_id
    if name:
        params["name"] = name
    if city:
        params["city"] = city
    if country:
        params["country"] = country
    if company_name:
        params["company_name"] = company_name

    data = await get("/jobs/search", params)

    if isinstance(data, dict) and "data" in data:
        results = data["data"]
    elif isinstance(data, list):
        results = data
    else:
        results = [data] if data else []

    return results[:limit]


async def get_job(job_slug: str) -> dict:
    """Get a single job by slug/ID."""
    return await get(f"/jobs/{job_slug}")
