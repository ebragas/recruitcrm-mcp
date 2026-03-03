"""HTTP client for the Recruit CRM API."""

import logging
import os
import time
from typing import Any

import anyio
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


def init_client() -> None:
    """Initialize the shared AsyncClient. Call during server startup."""
    global _client
    if _client is None:
        _client = httpx.AsyncClient()


async def aclose_client() -> None:
    """Close the shared AsyncClient. Call on application shutdown."""
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


def _get_client() -> httpx.AsyncClient:
    """Return the shared AsyncClient, which must be initialized first."""
    if _client is None:
        raise RuntimeError("HTTP client not initialized — call init_client() first")
    return _client


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
    client = _get_client()
    url = f"{API_BASE}{path}"
    kwargs = {"headers": _headers(), "params": params, "timeout": 30.0}

    resp = await client.get(url, **kwargs)

    if resp.status_code == 429:
        wait = _parse_retry_after(resp)
        logger.warning("Rate limited on %s — retrying in %.1fs", path, wait)
        await anyio.sleep(wait)
        resp = await client.get(url, **kwargs)

    resp.raise_for_status()
    return resp.json()


def _extract_results(data: Any) -> list[dict]:
    """Normalize API responses into a flat list of records."""
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    if isinstance(data, list):
        return data
    return [data] if data else []


async def search_candidates(
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    state: str | None = None,
    country: str | None = None,
    created_from: str | None = None,
    created_to: str | None = None,
    updated_from: str | None = None,
    updated_to: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """Search for candidates using available filters.

    When any filter is provided, uses ``/candidates/search``.
    When no filters are provided, falls back to ``/candidates`` (paginated list).
    """
    filters: dict[str, Any] = {}
    if first_name:
        filters["first_name"] = first_name
    if last_name:
        filters["last_name"] = last_name
    if email:
        filters["email"] = email
    if state:
        filters["state"] = state
    if country:
        filters["country"] = country
    if created_from:
        filters["created_from"] = created_from
    if created_to:
        filters["created_to"] = created_to
    if updated_from:
        filters["updated_from"] = updated_from
    if updated_to:
        filters["updated_to"] = updated_to

    if filters:
        data = await get("/candidates/search", filters)
    else:
        data = await get("/candidates", {"limit": limit})

    return _extract_results(data)[:limit]


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
    return _extract_results(data)[:limit]


async def search_jobs(
    status: str | None = None,
    name: str | None = None,
    city: str | None = None,
    country: str | None = None,
    company_name: str | None = None,
    created_from: str | None = None,
    created_to: str | None = None,
    updated_from: str | None = None,
    updated_to: str | None = None,
    owner_id: int | None = None,
    limit: int = 20,
) -> list[dict]:
    """Search for jobs via the /jobs/search endpoint.

    Filters are optional; the API returns an empty list when none are provided.

    ``status`` accepts a label string (e.g. 'Open', 'Closed') which is
    mapped to the integer ID the API expects.
    Date params use YYYY-MM-DD format.
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
    if created_from:
        params["created_from"] = created_from
    if created_to:
        params["created_to"] = created_to
    if updated_from:
        params["updated_from"] = updated_from
    if updated_to:
        params["updated_to"] = updated_to
    if owner_id is not None:
        params["owner_id"] = owner_id

    data = await get("/jobs/search", params)
    return _extract_results(data)[:limit]


async def get_job(job_slug: str) -> dict:
    """Get a single job by slug/ID."""
    return await get(f"/jobs/{job_slug}")


async def get_assigned_candidates(
    job_slug: str,
    status_id: str | None = None,
    limit: int = 25,
) -> list[dict]:
    """Get candidates assigned to a job with their hiring stage.

    Returns a list of ``{"candidate": {...}, "status": {...}}`` items.
    """
    params: dict[str, Any] = {"limit": limit}
    if status_id is not None:
        params["status_id"] = status_id
    data = await get(f"/jobs/{job_slug}/assigned-candidates", params)
    return _extract_results(data)[:limit]


async def list_users() -> list[dict]:
    """List all team members/users."""
    data = await get("/users")
    return _extract_results(data)
