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
_job_statuses: dict[str, int] | None = None


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
    """Close the shared AsyncClient and clear caches. Call on application shutdown."""
    global _client, _job_statuses
    if _client is not None:
        await _client.aclose()
        _client = None
    _job_statuses = None


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


def _extract_results(data: Any) -> list[dict]:
    """Normalize API response into a plain list of records."""
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    if isinstance(data, list):
        return data
    return [data] if data else []


async def find_candidates(
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    country: str | None = None,
    state: str | None = None,
    limit: int = 25,
) -> list[dict]:
    """Find candidates — searches when filters are provided, lists otherwise.

    With filters: calls ``/candidates/search`` (LIKE-style partial matching,
    AND logic).  Without filters: calls ``/candidates`` to browse.

    Both endpoints return 100 results per page minimum; ``limit`` is
    enforced client-side.
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

    if params:
        data = await get("/candidates/search", params)
    else:
        data = await get("/candidates", {"per_page": limit})

    return _extract_results(data)[:limit]


async def get_candidate(candidate_slug: str) -> dict:
    """Get a single candidate by slug/ID."""
    return await get(f"/candidates/{candidate_slug}")


async def _get_job_status_id(label: str) -> int:
    """Resolve a job status label to its API ID, fetching the mapping on first use."""
    global _job_statuses
    if _job_statuses is None:
        data = await get("/jobs-pipeline")
        _job_statuses = {s["label"].lower(): s["id"] for s in data}

    status_id = _job_statuses.get(label.lower())
    if status_id is None:
        valid = ", ".join(s.title() for s in sorted(_job_statuses))
        raise ValueError(f"Unknown job status {label!r}. Valid statuses: {valid}")
    if status_id == 0:
        raise ValueError(
            f"Cannot filter by status {label!r} — the API treats status ID 0 "
            "as no filter. Use get_job to check individual job statuses."
        )
    return status_id


async def find_jobs(
    name: str | None = None,
    status: str | None = None,
    city: str | None = None,
    country: str | None = None,
    company_name: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """Find jobs — searches when filters are provided, lists otherwise.

    With filters: calls ``/jobs/search`` (LIKE-style partial matching,
    AND logic).  Without filters: calls ``/jobs`` to browse.

    ``status`` accepts a label string (e.g. "Open", "On Hold") which is
    resolved to the API's integer ID via ``/jobs-pipeline``.

    Both endpoints return at least 15-100 results per page; ``limit`` is
    enforced client-side.
    """
    params: dict[str, Any] = {}
    if name:
        params["name"] = name
    if status:
        params["job_status"] = await _get_job_status_id(status)
    if city:
        params["city"] = city
    if country:
        params["country"] = country
    if company_name:
        params["company_name"] = company_name

    if params:
        data = await get("/jobs/search", params)
    else:
        data = await get("/jobs", {"per_page": limit})

    return _extract_results(data)[:limit]


async def get_job(job_slug: str) -> dict:
    """Get a single job by slug/ID."""
    return await get(f"/jobs/{job_slug}")
