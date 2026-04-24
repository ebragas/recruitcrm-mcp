"""HTTP client for the Recruit CRM API."""

import logging
import os
import time
from typing import Any

import anyio
import httpx

logger = logging.getLogger(__name__)


class RecruitCrmError(RuntimeError):
    """Structured error raised for non-2xx responses from the Recruit CRM API.

    Exposes the HTTP status and the parsed body (when JSON) so callers
    — including FastMCP tool surfaces — can show field-level validation errors.
    """

    def __init__(self, status: int, body: Any, method: str, path: str) -> None:
        self.status = status
        self.body = body
        self.method = method
        self.path = path
        super().__init__(f"{method} {path} -> {status}: {body!r}")


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


async def _request(
    method: str,
    path: str,
    data: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    form: dict[str, Any] | None = None,
    files: dict[str, Any] | None = None,
) -> Any:
    """Send an HTTP request to the Recruit CRM API.

    Handles auth headers, rate-limit retry (429), and response parsing.
    Returns parsed JSON, or ``None`` when the response body is empty.

    When ``files`` is provided the request is sent as ``multipart/form-data`` —
    JSON-encoded ``data`` and multipart are mutually exclusive because httpx
    auto-sets ``Content-Type`` based on the body shape.
    """
    http = _get_client()
    url = f"{API_BASE}{path}"
    kwargs: dict[str, Any] = {"headers": _headers(), "params": params, "timeout": 30.0}
    if files is not None:
        kwargs["data"] = form or {}
        kwargs["files"] = files
    elif data is not None:
        kwargs["json"] = data

    resp = await http.request(method, url, **kwargs)

    if resp.status_code == 429:
        wait = _parse_retry_after(resp)
        logger.warning("Rate limited on %s — retrying in %.1fs", path, wait)
        await anyio.sleep(wait)
        resp = await http.request(method, url, **kwargs)

    if not (200 <= resp.status_code < 300):
        if resp.content:
            try:
                body: Any = resp.json()
            except ValueError:
                body = resp.text
        else:
            body = None
        raise RecruitCrmError(resp.status_code, body, method, path)

    if resp.content:
        return resp.json()
    return None


async def get(path: str, params: dict[str, Any] | None = None) -> Any:
    """Make a GET request to the Recruit CRM API."""
    return await _request("GET", path, params=params)


async def post(
    path: str,
    data: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
) -> Any:
    """Make a POST request to the Recruit CRM API with a JSON body."""
    return await _request("POST", path, data=data, params=params)


async def delete(path: str, params: dict[str, Any] | None = None) -> Any:
    """Make a DELETE request to the Recruit CRM API."""
    return await _request("DELETE", path, params=params)


async def post_multipart(
    path: str,
    form: dict[str, Any],
    files: dict[str, Any],
    params: dict[str, Any] | None = None,
) -> Any:
    """Make a multipart/form-data POST. ``files`` is a dict of httpx-shaped tuples
    (see https://www.python-httpx.org/multipart/). Form fields and files are
    sent together; ``Content-Type`` is auto-set by httpx."""
    return await _request("POST", path, params=params, form=form, files=files)


def _extract_results(data: Any) -> list[dict]:
    """Normalize API responses into a flat list of records."""
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    if isinstance(data, list):
        return data
    return [data] if data else []


def _join(values: list[str] | list[int] | None) -> str | None:
    """Return a comma-separated string or ``None`` when the input is empty/None.

    Accepts strings or ints so callers can pass user ID lists without a manual
    ``[str(x) for x in ...]`` pre-pass.
    """
    if not values:
        return None
    return ",".join(str(v) for v in values)


def _associations_to_payload(associated: Any) -> dict[str, str]:
    """Flatten an ``Associations`` model to the API's ``associated_*`` payload keys.

    Omits empty lists entirely so callers can merge the result directly into a
    create payload without a second ``is not None`` sweep.
    """
    pairs = {
        "associated_candidates": associated.candidates,
        "associated_companies": associated.companies,
        "associated_contacts": associated.contacts,
        "associated_jobs": associated.jobs,
        "associated_deals": associated.deals,
    }
    return {k: joined for k, v in pairs.items() if (joined := _join(v)) is not None}


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


async def search_contacts(
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    linkedin: str | None = None,
    contact_number: str | None = None,
    company_slug: str | None = None,
    created_from: str | None = None,
    created_to: str | None = None,
    updated_from: str | None = None,
    updated_to: str | None = None,
    owner_id: int | None = None,
    limit: int = 10,
) -> list[dict]:
    """Search for contacts using available filters.

    When any filter is provided, uses ``/contacts/search``.
    When no filters are provided, falls back to ``/contacts`` (paginated list).
    """
    filters: dict[str, Any] = {}
    if first_name:
        filters["first_name"] = first_name
    if last_name:
        filters["last_name"] = last_name
    if email:
        filters["email"] = email
    if linkedin:
        filters["linkedin"] = linkedin
    if contact_number:
        filters["contact_number"] = contact_number
    if company_slug:
        filters["company_slug"] = company_slug
    if created_from:
        filters["created_from"] = created_from
    if created_to:
        filters["created_to"] = created_to
    if updated_from:
        filters["updated_from"] = updated_from
    if updated_to:
        filters["updated_to"] = updated_to
    if owner_id is not None:
        filters["owner_id"] = owner_id

    if filters:
        data = await get("/contacts/search", filters)
    else:
        data = await get("/contacts", {"limit": limit})

    return _extract_results(data)[:limit]


async def get_contact(contact_slug: str) -> dict:
    """Get a single contact by slug/ID."""
    return await get(f"/contacts/{contact_slug}")


async def search_companies(
    company_name: str | None = None,
    created_from: str | None = None,
    created_to: str | None = None,
    updated_from: str | None = None,
    updated_to: str | None = None,
    owner_id: int | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    exact_search: bool | None = None,
    limit: int = 10,
) -> list[dict]:
    """Search for companies using available filters.

    When any filter is provided, uses ``/companies/search``.
    When no filters are provided, falls back to ``/companies`` (paginated list).
    ``sort_by`` accepts ``createdon`` or ``updatedon``.
    ``sort_order`` accepts ``asc`` or ``desc``.
    """
    filters: dict[str, Any] = {}
    if company_name:
        filters["company_name"] = company_name
    if created_from:
        filters["created_from"] = created_from
    if created_to:
        filters["created_to"] = created_to
    if updated_from:
        filters["updated_from"] = updated_from
    if updated_to:
        filters["updated_to"] = updated_to
    if owner_id is not None:
        filters["owner_id"] = owner_id
    if sort_by:
        filters["sort_by"] = sort_by
    if sort_order:
        filters["sort_order"] = sort_order
    if exact_search is not None:
        filters["exact_search"] = "true" if exact_search else "false"

    if filters:
        data = await get("/companies/search", filters)
    else:
        data = await get("/companies", {"limit": limit})

    return _extract_results(data)[:limit]


async def get_company(company_slug: str) -> dict:
    """Get a single company by slug."""
    return await get(f"/companies/{company_slug}")


async def search_notes(
    added_from: str | None = None,
    added_to: str | None = None,
    updated_from: str | None = None,
    updated_to: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """Search for notes using available filters.

    When any filter is provided, uses ``/notes/search``.
    When no filters are provided, falls back to ``/notes`` (paginated list).

    Note: the API uses ``added_from``/``added_to`` instead of
    ``created_from``/``created_to``.
    """
    filters: dict[str, Any] = {}
    if added_from:
        filters["added_from"] = added_from
    if added_to:
        filters["added_to"] = added_to
    if updated_from:
        filters["updated_from"] = updated_from
    if updated_to:
        filters["updated_to"] = updated_to

    if filters:
        data = await get("/notes/search", filters)
    else:
        data = await get("/notes", {"limit": limit})

    return _extract_results(data)[:limit]


async def get_note(note_id: int | str) -> dict:
    """Get a single note by ID."""
    return await get(f"/notes/{note_id}")


async def search_tasks(
    title: str | None = None,
    created_from: str | None = None,
    created_to: str | None = None,
    updated_from: str | None = None,
    updated_to: str | None = None,
    starting_from: str | None = None,
    starting_to: str | None = None,
    owner_id: int | None = None,
    limit: int = 10,
) -> list[dict]:
    """Search for tasks using available filters.

    When any filter is provided, uses ``/tasks/search``.
    When no filters are provided, falls back to ``/tasks`` (paginated list).
    """
    filters: dict[str, Any] = {}
    if title:
        filters["title"] = title
    if created_from:
        filters["created_from"] = created_from
    if created_to:
        filters["created_to"] = created_to
    if updated_from:
        filters["updated_from"] = updated_from
    if updated_to:
        filters["updated_to"] = updated_to
    if starting_from:
        filters["starting_from"] = starting_from
    if starting_to:
        filters["starting_to"] = starting_to
    if owner_id is not None:
        filters["owner_id"] = owner_id

    if filters:
        data = await get("/tasks/search", filters)
    else:
        data = await get("/tasks", {"limit": limit})

    return _extract_results(data)[:limit]


async def get_task(task_id: int | str) -> dict:
    """Get a single task by ID."""
    return await get(f"/tasks/{task_id}")


async def search_meetings(
    title: str | None = None,
    created_from: str | None = None,
    created_to: str | None = None,
    updated_from: str | None = None,
    updated_to: str | None = None,
    starting_from: str | None = None,
    starting_to: str | None = None,
    owner_id: int | None = None,
    limit: int = 10,
) -> list[dict]:
    """Search for meetings using available filters.

    When any filter is provided, uses ``/meetings/search``.
    When no filters are provided, falls back to ``/meetings`` (paginated list).
    """
    filters: dict[str, Any] = {}
    if title:
        filters["title"] = title
    if created_from:
        filters["created_from"] = created_from
    if created_to:
        filters["created_to"] = created_to
    if updated_from:
        filters["updated_from"] = updated_from
    if updated_to:
        filters["updated_to"] = updated_to
    if starting_from:
        filters["starting_from"] = starting_from
    if starting_to:
        filters["starting_to"] = starting_to
    if owner_id is not None:
        filters["owner_id"] = owner_id

    if filters:
        data = await get("/meetings/search", filters)
    else:
        data = await get("/meetings", {"limit": limit})

    return _extract_results(data)[:limit]


async def get_meeting(meeting_id: int | str) -> dict:
    """Get a single meeting by ID."""
    return await get(f"/meetings/{meeting_id}")


async def list_users() -> list[dict]:
    """List all team members/users."""
    data = await get("/users")
    return _extract_results(data)


# ---------------------------------------------------------------------------
# Lookup endpoints
# ---------------------------------------------------------------------------


async def list_note_types() -> list[dict]:
    """List all note types.

    Response shape is already ``{id, label}``; no normalization needed.
    """
    data = await get("/note-types")
    return _extract_results(data)


async def list_meeting_types() -> list[dict]:
    """List all meeting types.

    Response shape is already ``{id, label}``; no normalization needed.
    """
    data = await get("/meeting-types")
    return _extract_results(data)


async def list_task_types() -> list[dict]:
    """List all task types.

    Response shape is already ``{id, label}``; no normalization needed.
    """
    data = await get("/task-types")
    return _extract_results(data)


async def list_hiring_pipelines() -> list[dict]:
    """List all hiring pipelines.

    Pipeline ID ``0`` is the master hiring pipeline. The API returns
    ``{id, name}`` — we remap ``name`` to ``label`` for LookupItem consistency.
    """
    data = await get("/hiring-pipelines")
    raw = _extract_results(data)
    return [{"id": item.get("id"), "label": item.get("name") or ""} for item in raw]


async def list_hiring_pipeline_stages(pipeline_id: int) -> list[dict]:
    """List hiring pipeline stages for a given pipeline ID.

    Use ``pipeline_id=0`` for the master hiring pipeline. The live API
    returns ``{status_id, label}`` (despite docs naming the field ``stage_id``);
    we remap ``status_id`` to ``id`` for LookupItem consistency.
    """
    data = await get(f"/hiring-pipelines/{pipeline_id}")
    raw = _extract_results(data)
    return [{"id": item.get("status_id"), "label": item.get("label") or ""} for item in raw]


async def list_contact_stages() -> list[dict]:
    """List sales pipeline stages (contact stages).

    The API returns ``{stage_id, label}`` — we remap ``stage_id`` to ``id``
    for LookupItem consistency.
    """
    data = await get("/sales-pipeline")
    raw = _extract_results(data)
    return [{"id": item.get("stage_id"), "label": item.get("label") or ""} for item in raw]


async def list_industries() -> list[dict]:
    """List all industries.

    The API returns ``{industry_id, label}`` — we remap ``industry_id`` to
    ``id`` for LookupItem consistency.
    """
    data = await get("/industries")
    raw = _extract_results(data)
    return [
        {"id": item.get("industry_id"), "label": item.get("label") or ""}
        for item in raw
    ]


def _normalize_custom_field(item: dict) -> dict:
    """Map custom-field records from ``field_id``/``field_name`` to ``id``/``label``.

    Preserves other keys (``field_type``, ``entity_type``, ``default_value``)
    so callers can still inspect them.
    """
    out = dict(item)
    out["id"] = item.get("field_id")
    out["label"] = item.get("field_name") or ""
    return out


async def list_company_custom_fields() -> list[dict]:
    """List all company custom fields."""
    data = await get("/custom-fields/companies")
    return [_normalize_custom_field(item) for item in _extract_results(data)]


async def list_contact_custom_fields() -> list[dict]:
    """List all contact custom fields."""
    data = await get("/custom-fields/contacts")
    return [_normalize_custom_field(item) for item in _extract_results(data)]


async def list_job_custom_fields() -> list[dict]:
    """List all job custom fields."""
    data = await get("/custom-fields/jobs")
    return [_normalize_custom_field(item) for item in _extract_results(data)]


async def list_candidate_custom_fields() -> list[dict]:
    """List all candidate custom fields."""
    data = await get("/custom-fields/candidates")
    return [_normalize_custom_field(item) for item in _extract_results(data)]


# ---------------------------------------------------------------------------
# Write endpoints
# ---------------------------------------------------------------------------


async def create_meeting(payload: dict[str, Any]) -> dict:
    """POST /v1/meetings — see docs/api-reference/creates-a-new-meeting.md."""
    return await post("/meetings", payload) or {}


async def create_note(payload: dict[str, Any]) -> dict:
    """POST /v1/notes — see docs/api-reference/creates-a-new-note.md."""
    return await post("/notes", payload) or {}


async def create_task(payload: dict[str, Any]) -> dict:
    """POST /v1/tasks — see docs/api-reference/creates-a-new-task.md."""
    return await post("/tasks", payload) or {}


async def update_task(task_id: int, patch: dict[str, Any]) -> dict:
    """POST /tasks/{id} — partial update. See edit-task.md.

    Per edit-task.md every body field is optional; the API preserves fields
    omitted from the payload. Non-None values in ``patch`` are sent as-is.
    Fetch-merge-POST was tried earlier but re-posting the read shape (e.g.
    ``task_type`` as nested object, ``associated_*`` as arrays) yields 422
    because the edit endpoint expects scalar ``task_type_id``/``owner_id``
    and comma-separated ``associated_*`` strings.
    """
    clean = {k: v for k, v in patch.items() if v is not None}
    result = await post(f"/tasks/{task_id}", clean)
    return result or {}


# ---------------------------------------------------------------------------
# CRUD write endpoints — companies / contacts / jobs / candidates
# ---------------------------------------------------------------------------


async def create_company(payload: dict[str, Any]) -> dict:
    """POST /v1/companies — create a new company record."""
    return await post("/companies", payload) or {}


async def update_company(company_slug: str, patch: dict[str, Any]) -> dict:
    """POST /companies/{slug} — partial update. See edit-a-company.md.

    Per edit-a-company.md every body field is optional in practice; the API
    preserves fields omitted from the payload. Non-None values in ``patch``
    are sent as-is. Fetch-merge-POST was tried earlier but re-posting the
    read shape yields 422 because the edit endpoint expects scalar IDs
    (e.g. ``owner_id``) and comma-separated string keys, not the nested
    objects returned by GET.
    """
    clean = {k: v for k, v in patch.items() if v is not None}
    result = await post(f"/companies/{company_slug}", clean)
    return result or {}


async def create_contact(payload: dict[str, Any]) -> dict:
    """POST /v1/contacts — create a new contact record."""
    return await post("/contacts", payload) or {}


async def update_contact(contact_slug: str, patch: dict[str, Any]) -> dict:
    """POST /contacts/{slug} — partial update. See edit-a-contact.md.

    Per edit-a-contact.md every body field is optional; the API preserves
    fields omitted from the payload. Non-None values in ``patch`` are sent
    as-is. Fetch-merge-POST was tried earlier but re-posting the read shape
    yields 422 because the edit endpoint expects scalar ``owner_id``/
    ``stage_id`` and comma-separated ``company_slug`` rather than the nested
    objects/arrays returned by GET.
    """
    clean = {k: v for k, v in patch.items() if v is not None}
    result = await post(f"/contacts/{contact_slug}", clean)
    return result or {}


async def create_job(payload: dict[str, Any]) -> dict:
    """POST /v1/jobs — create a new job requisition."""
    return await post("/jobs", payload) or {}


async def update_job(job_slug: str, patch: dict[str, Any]) -> dict:
    """POST /jobs/{slug} — partial update. See edit-a-job.md.

    Per edit-a-job.md every body field is optional; the API preserves fields
    omitted from the payload. Non-None values in ``patch`` are sent as-is.
    Fetch-merge-POST was tried earlier but re-posting the read shape yields
    422 because the edit endpoint expects scalar ``job_status``/``owner_id``
    and comma-separated ``collaborator_*`` strings rather than the nested
    objects/arrays returned by GET.
    """
    clean = {k: v for k, v in patch.items() if v is not None}
    result = await post(f"/jobs/{job_slug}", clean)
    return result or {}


async def create_candidate(payload: dict[str, Any]) -> dict:
    """POST /v1/candidates — create a new candidate record."""
    return await post("/candidates", payload) or {}


async def update_candidate(candidate_slug: str, patch: dict[str, Any]) -> dict:
    """POST /candidates/{slug} — partial update. See edit-a-candidate.md.

    Per edit-a-candidate.md every body field is optional; the API preserves
    fields omitted from the payload. Non-None values in ``patch`` are sent
    as-is. Fetch-merge-POST was tried earlier but re-posting the read shape
    yields 422 because the edit endpoint expects scalar ``owner_id`` and
    other write-shape keys rather than the nested objects (e.g. ``resume``,
    ``current_organization``) returned by GET.
    """
    clean = {k: v for k, v in patch.items() if v is not None}
    result = await post(f"/candidates/{candidate_slug}", clean)
    return result or {}


# ---------------------------------------------------------------------------
# Meeting edit / note delete
# ---------------------------------------------------------------------------


async def update_meeting(meeting_id: int, patch: dict[str, Any]) -> dict:
    """POST /meetings/{id} — partial update. See edit-meeting.md.

    Per edit-meeting.md every body field is optional; the API preserves
    fields omitted from the payload. Non-None values in ``patch`` are sent
    as-is. Fetch-merge-POST was tried earlier but re-posting the read shape
    yields 422 because the edit endpoint expects scalar ``meeting_type_id``/
    ``owner_id`` and comma-separated ``associated_*`` strings rather than
    the nested objects/arrays returned by GET.
    """
    clean = {k: v for k, v in patch.items() if v is not None}
    result = await post(f"/meetings/{meeting_id}", clean)
    return result or {}


async def delete_note(note_id: int) -> None:
    """DELETE /v1/notes/{id}."""
    await delete(f"/notes/{note_id}")


# ---------------------------------------------------------------------------
# Assignment trio — candidate/job linkage
# ---------------------------------------------------------------------------


async def assign_candidate(candidate_slug: str, job_slug: str) -> dict:
    """POST /v1/candidates/{candidate_slug}/assign?job_slug={job_slug}.

    The target job is passed as a query param, NOT in the body.
    """
    return await post(
        f"/candidates/{candidate_slug}/assign",
        params={"job_slug": job_slug},
    ) or {}


async def unassign_candidate(candidate_slug: str, job_slug: str) -> dict:
    """POST /v1/candidates/{candidate_slug}/unassign?job_slug={job_slug}.

    The target job is passed as a query param, NOT in the body.
    """
    return await post(
        f"/candidates/{candidate_slug}/unassign",
        params={"job_slug": job_slug},
    ) or {}


async def update_hiring_stage(
    candidate_slug: str,
    job_slug: str,
    body: dict[str, Any],
) -> dict:
    """POST /v1/candidates/{candidate_slug}/hiring-stages/{job_slug}.

    Both slugs are in the path (note the plural ``hiring-stages``).
    Body carries ``status_id`` plus optional ``remark``/``stage_date``/
    ``updated_by``/``create_placement``.
    """
    return await post(
        f"/candidates/{candidate_slug}/hiring-stages/{job_slug}",
        body,
    ) or {}


# ---------------------------------------------------------------------------
# File upload
# ---------------------------------------------------------------------------


async def upload_file(
    file_url: str,
    related_to: str,
    related_to_type: str,
    folder: str,
) -> dict:
    """POST /v1/files — multipart upload of a file by public URL.

    The ``files[]`` form field accepts either a public URL or a file upload;
    we support the URL form here. Uploading binary files would require the
    tool caller to stream bytes, which MCP doesn't expose cleanly.
    """
    form = {
        "related_to": related_to,
        "related_to_type": related_to_type,
        "folder": folder,
    }
    # httpx multipart text-part shape: (filename, content). Passing filename=None
    # sends the value as a plain form field under the `files[]` key.
    files = {"files[]": (None, file_url)}
    return await post_multipart("/files", form, files) or {}
