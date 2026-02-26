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
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    country: str | None = None,
    state: str | None = None,
    limit: int = 25,
) -> list[dict]:
    """Search for candidates via the /candidates/search endpoint.

    At least one filter must be provided — the API returns an empty list
    when called with no filters.  All filters use like-matching by default.

    Note: the search endpoint does not accept ``per_page``; it always
    returns 100 results per page.  We enforce ``limit`` client-side.
    """
    params: dict[str, Any] = {}
    if first_name:
        params["first_name"] = first_name
    if last_name:
        params["last_name"] = last_name
    if email:
        params["email"] = email
    if country:
        params["country"] = country
    if state:
        params["state"] = state

    data = await get("/candidates/search", params)

    # API returns paginated response with "data" key, or [] when no filters
    if isinstance(data, dict) and "data" in data:
        results = data["data"]
    elif isinstance(data, list):
        results = data
    else:
        results = [data] if data else []

    # Search endpoint always returns 100/page, so enforce limit client-side
    return results[:limit]


async def list_candidates(limit: int = 25) -> list[dict]:
    """List candidates via the /candidates endpoint (no filtering).

    Use this when you need to browse candidates without specific filters.
    The API always returns at least 100 per page; ``limit`` is enforced
    client-side.
    """
    data = await get("/candidates", {"per_page": limit})

    if isinstance(data, dict) and "data" in data:
        results = data["data"]
    elif isinstance(data, list):
        results = data
    else:
        results = [data] if data else []

    return results[:limit]


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
        results = data["data"]
    elif isinstance(data, list):
        results = data
    else:
        results = [data] if data else []

    # API ignores per_page below its minimum (15), so enforce limit client-side
    return results[:limit]


async def get_job(job_slug: str) -> dict:
    """Get a single job by slug/ID."""
    return await get(f"/jobs/{job_slug}")
