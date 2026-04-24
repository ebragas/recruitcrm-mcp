"""Recruit CRM MCP server."""

import logging
import os
from contextlib import asynccontextmanager
from importlib.metadata import version, PackageNotFoundError

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from recruit_crm_mcp import client
from recruit_crm_mcp.client import RecruitCrmError
from recruit_crm_mcp.models import (
    AssignedCandidateSummary,
    Associations,
    CandidateSummary,
    CompanySummary,
    ContactSummary,
    CustomFieldValue,
    EntityRef,
    JobSummary,
    LookupItem,
    MeetingSummary,
    NoteSummary,
    TaskSummary,
    UserSummary,
    WriteResult,
)

logger = logging.getLogger(__name__)

try:
    __version__ = version("recruit-crm-mcp")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"


@asynccontextmanager
async def _lifespan(server: FastMCP):
    client.init_client()
    yield
    await client.aclose_client()


mcp = FastMCP("Recruit CRM", lifespan=_lifespan)


def _write_result_from(kind: str, response: dict) -> WriteResult:
    """Build a ``WriteResult`` from a Recruit CRM create/update response."""
    # Explicit None check — some endpoints may return integer id 0 in edge cases,
    # which `or`-chaining would incorrectly treat as missing.
    raw_id = response.get("id")
    if raw_id is None:
        raw_id = response.get("slug")
    if raw_id is None:
        # Neither id nor slug returned — callers get WriteResult.id="" which is
        # useless for follow-up calls. Log loudly so the symptom surfaces in ops
        # rather than silently propagating a broken reference.
        logger.warning(
            "%s write returned no id/slug — response keys: %s",
            kind, sorted(response.keys()) if isinstance(response, dict) else type(response).__name__,
        )
    # Different entities label the same concept with different field names;
    # walk the fallback chain so WriteResult.title populates consistently.
    person_name = f"{response.get('first_name') or ''} {response.get('last_name') or ''}".strip()
    title = (
        response.get("title")
        or response.get("name")
        or response.get("company_name")
        or person_name
        or None
    )
    return WriteResult(
        kind=kind,
        id="" if raw_id is None else str(raw_id),
        title=title,
        url=response.get("resource_url"),
    )


def _build_payload(
    fields: dict,
    custom_fields: list[CustomFieldValue] | None = None,
) -> dict:
    """Assemble a create/update payload.

    Drops ``None`` values from ``fields`` (MCP tool kwargs that weren't passed).
    ``custom_fields`` is forwarded whenever explicitly provided: ``None`` omits
    the key, while an empty list serializes as ``"custom_fields": []`` so
    callers can intentionally clear all existing custom-field values.
    """
    payload = {k: v for k, v in fields.items() if v is not None}
    if custom_fields is not None:
        payload["custom_fields"] = [cf.model_dump() for cf in custom_fields]
    return payload


def _reraise_as_tool_error(exc: RecruitCrmError) -> None:
    """Surface RCRM field-level validation errors through FastMCP cleanly.

    FastMCP would otherwise stringify the RuntimeError repr — users see the
    body dict as a Python string. Convert to ToolError so the message is a
    clean explanation the LLM can present or act on.
    """
    body = exc.body
    if isinstance(body, dict):
        # Flatten "{'field': ['msg1', 'msg2']}" -> "field: msg1, msg2"
        field_errors = "; ".join(
            f"{k}: {', '.join(v) if isinstance(v, list) else v}"
            for k, v in body.items()
        )
        raise ToolError(
            f"{exc.method} {exc.path} failed ({exc.status}): {field_errors}"
        ) from exc
    raise ToolError(
        f"{exc.method} {exc.path} failed ({exc.status}): {body}"
    ) from exc


@mcp.tool()
def ping() -> dict:
    """Check that the Recruit CRM MCP server is running and configured."""
    has_key = bool(os.environ.get("RECRUIT_CRM_API_KEY"))
    return {
        "status": "ok",
        "version": __version__,
        "api_configured": has_key,
    }


@mcp.tool()
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
) -> list[CandidateSummary]:
    """Search for candidates by name, email, location, or date range.

    Provide at least one filter for targeted results. Filters are combined with AND logic.
    With no filters, returns a paginated list of recent candidates.
    Date params use YYYY-MM-DD format.
    Returns a list of matching candidate summaries.
    """
    results = await client.search_candidates(
        first_name=first_name,
        last_name=last_name,
        email=email,
        state=state,
        country=country,
        created_from=created_from,
        created_to=created_to,
        updated_from=updated_from,
        updated_to=updated_to,
        limit=limit,
    )
    return [CandidateSummary.from_api_response(c) for c in results]


@mcp.tool()
async def get_candidate(candidate_id: str) -> dict:
    """Get full profile details for a specific candidate by slug or ID."""
    return await client.get_candidate(candidate_id)


@mcp.tool()
async def list_jobs(limit: int = 20) -> list[JobSummary]:
    """List job requisitions without any filters.

    Returns jobs in reverse chronological order.
    Use search_jobs instead when you need to filter by status or other fields.
    """
    results = await client.list_jobs(limit=limit)
    return [JobSummary.from_api_response(j) for j in results]


@mcp.tool()
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
) -> list[JobSummary]:
    """Search for jobs by status, name, location, company, date range, or owner.

    Filters are optional and combined with AND logic.
    Status accepts a label: 'Open', 'On Hold', 'Closed', 'Placed', 'Canceled', 'Refill'.
    Date params use YYYY-MM-DD format.
    Use list_users to find valid owner_id values.
    With no filters, returns an empty list.
    """
    results = await client.search_jobs(
        status=status,
        name=name,
        city=city,
        country=country,
        company_name=company_name,
        created_from=created_from,
        created_to=created_to,
        updated_from=updated_from,
        updated_to=updated_to,
        owner_id=owner_id,
        limit=limit,
    )
    return [JobSummary.from_api_response(j) for j in results]


@mcp.tool()
async def get_job(job_id: str) -> dict:
    """Get full details for a specific job by slug or ID."""
    return await client.get_job(job_id)


@mcp.tool()
async def get_assigned_candidates(
    job_slug: str,
    status_id: str | None = None,
    limit: int = 25,
) -> list[AssignedCandidateSummary]:
    """Get candidates assigned to a specific job and their hiring stage.

    Returns candidate summaries with their current hiring status for the given job.
    Use status_id to filter by a specific hiring stage.
    """
    results = await client.get_assigned_candidates(
        job_slug=job_slug,
        status_id=status_id,
        limit=limit,
    )
    return [AssignedCandidateSummary.from_api_response(item) for item in results]


@mcp.tool()
async def get_contact(contact_slug: str) -> dict:
    """Get full details for a specific contact by slug."""
    return await client.get_contact(contact_slug)


@mcp.tool()
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
) -> list[ContactSummary]:
    """Search for contacts by name, email, company, or date range.

    Provide at least one filter for targeted results. Filters are combined with AND logic.
    With no filters, returns a paginated list of recent contacts.
    Date params use YYYY-MM-DD format.
    """
    results = await client.search_contacts(
        first_name=first_name,
        last_name=last_name,
        email=email,
        linkedin=linkedin,
        contact_number=contact_number,
        company_slug=company_slug,
        created_from=created_from,
        created_to=created_to,
        updated_from=updated_from,
        updated_to=updated_to,
        owner_id=owner_id,
        limit=limit,
    )
    return [ContactSummary.from_api_response(c) for c in results]


@mcp.tool()
async def get_company(company_slug: str) -> dict:
    """Get full details for a specific company by slug."""
    return await client.get_company(company_slug)


@mcp.tool()
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
) -> list[CompanySummary]:
    """Search for companies by name, date range, or owner.

    Provide at least one filter for targeted results. Filters are combined with AND logic.
    With no filters, returns a paginated list of recent companies.
    Date params use YYYY-MM-DD format.
    sort_by accepts 'createdon' or 'updatedon'. sort_order accepts 'asc' or 'desc'.
    Set exact_search=True for exact name matching (default is fuzzy/like matching).
    Use list_users to find valid owner_id values.
    """
    results = await client.search_companies(
        company_name=company_name,
        created_from=created_from,
        created_to=created_to,
        updated_from=updated_from,
        updated_to=updated_to,
        owner_id=owner_id,
        sort_by=sort_by,
        sort_order=sort_order,
        exact_search=exact_search,
        limit=limit,
    )
    return [CompanySummary.from_api_response(c) for c in results]


@mcp.tool()
async def get_note(note_id: int) -> dict:
    """Get full details for a specific note by ID."""
    return await client.get_note(note_id)


@mcp.tool()
async def search_notes(
    created_from: str | None = None,
    created_to: str | None = None,
    updated_from: str | None = None,
    updated_to: str | None = None,
    limit: int = 10,
) -> list[NoteSummary]:
    """Search for notes by date range.

    Provide at least one filter for targeted results. Filters are combined with AND logic.
    With no filters, returns a paginated list of recent notes.
    Date params use YYYY-MM-DD format.
    """
    results = await client.search_notes(
        added_from=created_from,
        added_to=created_to,
        updated_from=updated_from,
        updated_to=updated_to,
        limit=limit,
    )
    return [NoteSummary.from_api_response(n) for n in results]


@mcp.tool()
async def get_task(task_id: int) -> dict:
    """Get full details for a specific task by ID."""
    return await client.get_task(task_id)


@mcp.tool()
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
) -> list[TaskSummary]:
    """Search for tasks by title, date range, or owner.

    Provide at least one filter for targeted results. Filters are combined with AND logic.
    With no filters, returns a paginated list of recent tasks.
    Date params use YYYY-MM-DD format.
    Use list_users to find valid owner_id values.
    """
    results = await client.search_tasks(
        title=title,
        created_from=created_from,
        created_to=created_to,
        updated_from=updated_from,
        updated_to=updated_to,
        starting_from=starting_from,
        starting_to=starting_to,
        owner_id=owner_id,
        limit=limit,
    )
    return [TaskSummary.from_api_response(t) for t in results]


@mcp.tool()
async def get_meeting(meeting_id: int) -> dict:
    """Get full details for a specific meeting by ID."""
    return await client.get_meeting(meeting_id)


@mcp.tool()
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
) -> list[MeetingSummary]:
    """Search for meetings by title, date range, or owner.

    Provide at least one filter for targeted results. Filters are combined with AND logic.
    With no filters, returns a paginated list of recent meetings.
    Date params use YYYY-MM-DD format.
    Use list_users to find valid owner_id values.
    """
    results = await client.search_meetings(
        title=title,
        created_from=created_from,
        created_to=created_to,
        updated_from=updated_from,
        updated_to=updated_to,
        starting_from=starting_from,
        starting_to=starting_to,
        owner_id=owner_id,
        limit=limit,
    )
    return [MeetingSummary.from_api_response(m) for m in results]


@mcp.tool()
async def list_users() -> list[UserSummary]:
    """List all team members/users.

    Useful for discovering owner IDs to use with the search_jobs owner_id filter.
    Returns id, name, email, and role for each user.
    """
    results = await client.list_users()
    return [UserSummary.from_api_response(u) for u in results]


@mcp.tool()
async def list_note_types() -> list[LookupItem]:
    """List all note types available in the account.

    Returns {id, label} pairs suitable for passing as note_type_id on note writes.
    """
    results = await client.list_note_types()
    return [LookupItem.from_api_response(item) for item in results]


@mcp.tool()
async def list_meeting_types() -> list[LookupItem]:
    """List all meeting types available in the account.

    Returns {id, label} pairs suitable for passing as meeting_type_id on meeting writes.
    """
    results = await client.list_meeting_types()
    return [LookupItem.from_api_response(item) for item in results]


@mcp.tool()
async def list_task_types() -> list[LookupItem]:
    """List all task types available in the account.

    Returns {id, label} pairs suitable for passing as task_type_id on task writes.
    """
    results = await client.list_task_types()
    return [LookupItem.from_api_response(item) for item in results]


@mcp.tool()
async def list_hiring_pipelines() -> list[LookupItem]:
    """List all hiring pipelines configured in the account.

    Pipeline ID 0 is the master hiring pipeline. Use list_hiring_pipeline_stages
    with the returned id to inspect stages for a specific pipeline.
    """
    results = await client.list_hiring_pipelines()
    return [LookupItem.from_api_response(item) for item in results]


@mcp.tool()
async def list_hiring_pipeline_stages(pipeline_id: int) -> list[LookupItem]:
    """List hiring pipeline stages for a given pipeline.

    Use pipeline_id=0 for the master hiring pipeline. Returns {id, label} stage
    entries suitable for filtering assigned candidates by hiring stage.
    """
    results = await client.list_hiring_pipeline_stages(pipeline_id)
    return [LookupItem.from_api_response(item) for item in results]


@mcp.tool()
async def list_contact_stages() -> list[LookupItem]:
    """List sales pipeline stages (contact stages).

    Returns {id, label} pairs for each stage in the sales pipeline.
    """
    results = await client.list_contact_stages()
    return [LookupItem.from_api_response(item) for item in results]


@mcp.tool()
async def list_industries() -> list[LookupItem]:
    """List all industries available in the account.

    Returns {id, label} pairs suitable for populating a company's industry_id.
    """
    results = await client.list_industries()
    return [LookupItem.from_api_response(item) for item in results]


@mcp.tool()
async def list_company_custom_fields() -> list[LookupItem]:
    """List all company custom fields defined in the account.

    Returns {id, label} pairs where id is the field_id and label is the field name.
    """
    results = await client.list_company_custom_fields()
    return [LookupItem.from_api_response(item) for item in results]


@mcp.tool()
async def list_contact_custom_fields() -> list[LookupItem]:
    """List all contact custom fields defined in the account.

    Returns {id, label} pairs where id is the field_id and label is the field name.
    """
    results = await client.list_contact_custom_fields()
    return [LookupItem.from_api_response(item) for item in results]


@mcp.tool()
async def list_job_custom_fields() -> list[LookupItem]:
    """List all job custom fields defined in the account.

    Returns {id, label} pairs where id is the field_id and label is the field name.
    """
    results = await client.list_job_custom_fields()
    return [LookupItem.from_api_response(item) for item in results]


@mcp.tool()
async def list_candidate_custom_fields() -> list[LookupItem]:
    """List all candidate custom fields defined in the account.

    Returns {id, label} pairs where id is the field_id and label is the field name.
    """
    results = await client.list_candidate_custom_fields()
    return [LookupItem.from_api_response(item) for item in results]


@mcp.tool()
async def log_meeting(
    title: str,
    start_date: str,
    end_date: str,
    related_to: EntityRef,
    attendee_contacts: list[str] | None = None,
    attendee_candidates: list[str] | None = None,
    attendee_users: list[int] | None = None,
    description: str | None = None,
    address: str | None = None,
    meeting_type_id: int | None = None,
    reminder: int = -1,
    owner_id: int | None = None,
    associated: Associations | None = None,
    do_not_send_calendar_invites: bool = True,
) -> WriteResult:
    """Log a meeting via POST /v1/meetings.

    Dates use ISO 8601 (e.g. ``2025-04-29T18:30:00Z``).
    ``related_to`` is the primary anchor entity. Use ``associated`` to cross-link
    the meeting to additional candidates/companies/contacts/jobs/deals.
    ``attendee_users`` expects integer user IDs; ``attendee_contacts`` and
    ``attendee_candidates`` expect slug strings.
    ``reminder`` accepts: -1 (no reminder), 0, 15, 30, 60, 120, 1440 (minutes before).
    ``do_not_send_calendar_invites`` defaults to True — safe for historical logging;
    set False to actually send invites to attendees.
    """
    payload = _build_payload({
        "title": title,
        "start_date": start_date,
        "end_date": end_date,
        "reminder": reminder,
        "related_to": related_to.id,
        "related_to_type": related_to.kind,
        "attendee_contacts": client._join(attendee_contacts),
        "attendee_candidates": client._join(attendee_candidates),
        "attendee_users": client._join(attendee_users),
        "description": description,
        "address": address,
        "meeting_type_id": meeting_type_id,
        "owner_id": owner_id,
        # API rejects JSON `false` with 422 — serialize to "1"/"0" strings instead.
        "do_not_send_calendar_invites": "1" if do_not_send_calendar_invites else "0",
    })
    if associated is not None:
        payload.update(client._associations_to_payload(associated))
    try:
        response = await client.create_meeting(payload)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("meeting", response)


@mcp.tool()
async def create_note(
    description: str,
    related_to: EntityRef,
    note_type_id: int | None = None,
    associated: Associations | None = None,
) -> WriteResult:
    """Create a note via POST /v1/notes.

    ``related_to`` is the primary anchor entity. Use ``associated`` to cross-link
    the note to additional candidates/companies/contacts/jobs/deals.
    """
    payload = _build_payload({
        "description": description,
        "related_to": related_to.id,
        "related_to_type": related_to.kind,
        "note_type_id": note_type_id,
    })
    if associated is not None:
        payload.update(client._associations_to_payload(associated))
    try:
        response = await client.create_note(payload)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("note", response)


@mcp.tool()
async def create_task(
    title: str,
    start_date: str,
    description: str | None = None,
    reminder: int = 1440,
    task_type_id: int | None = None,
    owner_id: int | None = None,
    related_to: EntityRef | None = None,
    associated: Associations | None = None,
) -> WriteResult:
    """Create a task via POST /v1/tasks.

    ``start_date`` uses ISO 8601 (e.g. ``2025-04-29T18:30:00Z``).
    ``related_to`` is optional but recommended for easy discovery.
    ``reminder`` accepts: -1 (no reminder), 0, 15, 30, 60, 1440 (minutes before);
    defaults to 1440 (1 day before).
    """
    fields: dict = {
        "title": title,
        "start_date": start_date,
        "reminder": reminder,
        "description": description,
        "task_type_id": task_type_id,
        "owner_id": owner_id,
    }
    if related_to is not None:
        fields["related_to"] = related_to.id
        fields["related_to_type"] = related_to.kind
    payload = _build_payload(fields)
    if associated is not None:
        payload.update(client._associations_to_payload(associated))
    try:
        response = await client.create_task(payload)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("task", response)


@mcp.tool()
async def update_task(
    task_id: int,
    title: str | None = None,
    start_date: str | None = None,
    description: str | None = None,
    status: str | None = None,
    task_type_id: int | None = None,
    owner_id: int | None = None,
) -> WriteResult:
    """Update an existing task via GET+merge+POST on /v1/tasks/{id}.

    Only non-None fields are forwarded; omitted fields are preserved.
    ``status`` accepts ``"o"`` (open) or ``"c"`` (complete).
    ``task_type_id`` is the integer ID from ``list_task_types``; omit to keep
    current type.
    """
    patch = _build_payload({
        "title": title,
        "start_date": start_date,
        "description": description,
        "status": status,
        "task_type_id": task_type_id,
        "owner_id": owner_id,
    })
    try:
        response = await client.update_task(task_id, patch)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("task", response)


# ---------------------------------------------------------------------------
# Company write tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_company(
    company_name: str,
    about_company: str | None = None,
    website: str | None = None,
    industry_id: int | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    linkedin: str | None = None,
    owner_id: int | None = None,
    custom_fields: list[CustomFieldValue] | None = None,
) -> WriteResult:
    """Create a company via POST /v1/companies.

    ``company_name`` is the only required field. Use ``list_industries`` to
    resolve ``industry_id`` and ``list_company_custom_fields`` to discover
    valid ``custom_fields`` field_ids.
    """
    payload = _build_payload(
        {
            "company_name": company_name,
            "about_company": about_company,
            "website": website,
            "industry_id": industry_id,
            "city": city,
            "state": state,
            "country": country,
            "linkedin": linkedin,
            "owner_id": owner_id,
        },
        custom_fields,
    )
    try:
        response = await client.create_company(payload)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("company", response)


@mcp.tool()
async def update_company(
    slug: str,
    company_name: str | None = None,
    about_company: str | None = None,
    website: str | None = None,
    industry_id: int | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    linkedin: str | None = None,
    owner_id: int | None = None,
    custom_fields: list[CustomFieldValue] | None = None,
) -> WriteResult:
    """Update a company via GET+merge+POST on /v1/companies/{slug}.

    Only non-None fields are forwarded; omitted fields are preserved from the
    current record (the API's required ``company_name`` is kept automatically).
    """
    patch = _build_payload(
        {
            "company_name": company_name,
            "about_company": about_company,
            "website": website,
            "industry_id": industry_id,
            "city": city,
            "state": state,
            "country": country,
            "linkedin": linkedin,
            "owner_id": owner_id,
        },
        custom_fields,
    )
    try:
        response = await client.update_company(slug, patch)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("company", response)


@mcp.tool()
async def set_company_custom_fields(
    slug: str,
    fields: list[CustomFieldValue],
) -> WriteResult:
    """Set custom-field values on a company without touching any standard fields.

    Thin wrapper over ``update_company`` — the edit endpoint accepts
    ``custom_fields`` inline (there is no separate associated-fields endpoint
    for companies).
    """
    return await update_company(slug=slug, custom_fields=fields)


# ---------------------------------------------------------------------------
# Contact write tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_contact(
    first_name: str,
    last_name: str,
    email: str | None = None,
    contact_number: str | None = None,
    designation: str | None = None,
    stage_id: int | None = None,
    company_slug: str | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    linkedin: str | None = None,
    owner_id: int | None = None,
    custom_fields: list[CustomFieldValue] | None = None,
) -> WriteResult:
    """Create a contact via POST /v1/contacts.

    ``first_name`` and ``last_name`` are required. ``company_slug`` accepts a
    comma-separated string for multi-company associations. Use
    ``list_contact_stages`` to resolve ``stage_id``.
    """
    payload = _build_payload(
        {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "contact_number": contact_number,
            "designation": designation,
            "stage_id": stage_id,
            "company_slug": company_slug,
            "city": city,
            "state": state,
            "country": country,
            "linkedin": linkedin,
            "owner_id": owner_id,
        },
        custom_fields,
    )
    try:
        response = await client.create_contact(payload)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("contact", response)


@mcp.tool()
async def update_contact(
    slug: str,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    contact_number: str | None = None,
    designation: str | None = None,
    stage_id: int | None = None,
    company_slug: str | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    linkedin: str | None = None,
    owner_id: int | None = None,
    custom_fields: list[CustomFieldValue] | None = None,
) -> WriteResult:
    """Update a contact via GET+merge+POST on /v1/contacts/{slug}.

    Only non-None fields are forwarded; omitted fields are preserved.
    """
    patch = _build_payload(
        {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "contact_number": contact_number,
            "designation": designation,
            "stage_id": stage_id,
            "company_slug": company_slug,
            "city": city,
            "state": state,
            "country": country,
            "linkedin": linkedin,
            "owner_id": owner_id,
        },
        custom_fields,
    )
    try:
        response = await client.update_contact(slug, patch)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("contact", response)


@mcp.tool()
async def set_contact_custom_fields(
    slug: str,
    fields: list[CustomFieldValue],
) -> WriteResult:
    """Set custom-field values on a contact without touching any standard fields."""
    return await update_contact(slug=slug, custom_fields=fields)


# ---------------------------------------------------------------------------
# Job write tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_job(
    name: str,
    company_slug: str,
    contact_slug: str,
    number_of_openings: int,
    currency_id: int,
    enable_job_application_form: int,
    job_description_text: str,
    job_status: int | None = None,
    job_location_type: int | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    min_annual_salary: int | None = None,
    max_annual_salary: int | None = None,
    owner_id: int | None = None,
    hiring_pipeline_id: int | None = None,
    note_for_candidates: str | None = None,
    custom_fields: list[CustomFieldValue] | None = None,
) -> WriteResult:
    """Create a job requisition via POST /v1/jobs.

    Seven fields are required: ``name``, ``company_slug``, ``contact_slug``,
    ``number_of_openings``, ``currency_id``, ``enable_job_application_form``,
    ``job_description_text``.

    ``job_status`` codes: 0=Closed, 1=Open, 2=On Hold, 3=Cancelled.
    ``job_location_type`` codes: 0=On-site, 1=Remote, 2=Hybrid.

    Use ``list_hiring_pipelines`` for ``hiring_pipeline_id`` and
    ``list_job_custom_fields`` for ``custom_fields``.
    """
    payload = _build_payload(
        {
            "name": name,
            "company_slug": company_slug,
            "contact_slug": contact_slug,
            "number_of_openings": number_of_openings,
            "currency_id": currency_id,
            "enable_job_application_form": enable_job_application_form,
            "job_description_text": job_description_text,
            "job_status": job_status,
            "job_location_type": job_location_type,
            "city": city,
            "state": state,
            "country": country,
            "min_annual_salary": min_annual_salary,
            "max_annual_salary": max_annual_salary,
            "owner_id": owner_id,
            "hiring_pipeline_id": hiring_pipeline_id,
            "note_for_candidates": note_for_candidates,
        },
        custom_fields,
    )
    try:
        response = await client.create_job(payload)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("job", response)


@mcp.tool()
async def update_job(
    slug: str,
    name: str | None = None,
    job_status: int | None = None,
    job_location_type: int | None = None,
    min_annual_salary: int | None = None,
    max_annual_salary: int | None = None,
    owner_id: int | None = None,
    note_for_candidates: str | None = None,
    custom_fields: list[CustomFieldValue] | None = None,
) -> WriteResult:
    """Update a job requisition via GET+merge+POST on /v1/jobs/{slug}.

    Only the fields most commonly edited are exposed; use the full ``create_job``
    surface area if you need to change other fields.
    """
    patch = _build_payload(
        {
            "name": name,
            "job_status": job_status,
            "job_location_type": job_location_type,
            "min_annual_salary": min_annual_salary,
            "max_annual_salary": max_annual_salary,
            "owner_id": owner_id,
            "note_for_candidates": note_for_candidates,
        },
        custom_fields,
    )
    try:
        response = await client.update_job(slug, patch)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("job", response)


@mcp.tool()
async def set_job_custom_fields(
    slug: str,
    fields: list[CustomFieldValue],
) -> WriteResult:
    """Set custom-field values on a job without touching any standard fields."""
    return await update_job(slug=slug, custom_fields=fields)


# ---------------------------------------------------------------------------
# Candidate write tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def create_candidate(
    first_name: str,
    last_name: str | None = None,
    email: str | None = None,
    contact_number: str | None = None,
    current_organization: str | None = None,
    current_organization_slug: str | None = None,
    current_status: str | None = None,
    position: str | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    salary_expectation: str | None = None,
    notice_period: int | None = None,
    available_from: str | None = None,
    linkedin: str | None = None,
    owner_id: int | None = None,
    custom_fields: list[CustomFieldValue] | None = None,
) -> WriteResult:
    """Create a candidate via POST /v1/candidates.

    ``first_name`` is the only required field. ``current_organization_slug``
    links the candidate to an existing company record; ``current_organization``
    is the free-text fallback.
    """
    payload = _build_payload(
        {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "contact_number": contact_number,
            "current_organization": current_organization,
            "current_organization_slug": current_organization_slug,
            "current_status": current_status,
            "position": position,
            "city": city,
            "state": state,
            "country": country,
            "salary_expectation": salary_expectation,
            "notice_period": notice_period,
            "available_from": available_from,
            "linkedin": linkedin,
            "owner_id": owner_id,
        },
        custom_fields,
    )
    try:
        response = await client.create_candidate(payload)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("candidate", response)


@mcp.tool()
async def update_candidate(
    slug: str,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    contact_number: str | None = None,
    current_organization: str | None = None,
    current_organization_slug: str | None = None,
    current_status: str | None = None,
    position: str | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    salary_expectation: str | None = None,
    notice_period: int | None = None,
    available_from: str | None = None,
    linkedin: str | None = None,
    owner_id: int | None = None,
    custom_fields: list[CustomFieldValue] | None = None,
) -> WriteResult:
    """Update a candidate via GET+merge+POST on /v1/candidates/{slug}.

    Only non-None fields are forwarded; omitted fields are preserved from the
    current record (the API's required ``first_name`` is kept automatically).
    """
    patch = _build_payload(
        {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "contact_number": contact_number,
            "current_organization": current_organization,
            "current_organization_slug": current_organization_slug,
            "current_status": current_status,
            "position": position,
            "city": city,
            "state": state,
            "country": country,
            "salary_expectation": salary_expectation,
            "notice_period": notice_period,
            "available_from": available_from,
            "linkedin": linkedin,
            "owner_id": owner_id,
        },
        custom_fields,
    )
    try:
        response = await client.update_candidate(slug, patch)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("candidate", response)


@mcp.tool()
async def set_candidate_custom_fields(
    slug: str,
    fields: list[CustomFieldValue],
) -> WriteResult:
    """Set custom-field values on a candidate without touching any standard fields."""
    return await update_candidate(slug=slug, custom_fields=fields)


# ---------------------------------------------------------------------------
# Meeting update / note delete
# ---------------------------------------------------------------------------


@mcp.tool()
async def update_meeting(
    meeting_id: int,
    title: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    description: str | None = None,
    address: str | None = None,
    meeting_type_id: int | None = None,
    reminder: int | None = None,
    owner_id: int | None = None,
    related_to: EntityRef | None = None,
    attendee_contacts: list[str] | None = None,
    attendee_candidates: list[str] | None = None,
    attendee_users: list[int] | None = None,
    associated: Associations | None = None,
    do_not_send_calendar_invites: bool | None = None,
) -> WriteResult:
    """Update a meeting via GET+merge+POST on /v1/meetings/{id}.

    Only non-None fields are forwarded; omitted fields are preserved. Attendee
    and association lists are joined into comma-separated strings to match the
    create-endpoint shape.
    """
    fields: dict = {
        "title": title,
        "start_date": start_date,
        "end_date": end_date,
        "description": description,
        "address": address,
        "meeting_type_id": meeting_type_id,
        "reminder": reminder,
        "owner_id": owner_id,
        # API rejects JSON `false` with 422 — serialize to "1"/"0" (None keeps the existing value).
        "do_not_send_calendar_invites": (
            None
            if do_not_send_calendar_invites is None
            else ("1" if do_not_send_calendar_invites else "0")
        ),
        "attendee_contacts": client._join(attendee_contacts),
        "attendee_candidates": client._join(attendee_candidates),
        "attendee_users": client._join(attendee_users),
    }
    if related_to is not None:
        fields["related_to"] = related_to.id
        fields["related_to_type"] = related_to.kind
    patch = _build_payload(fields)
    if associated is not None:
        patch.update(client._associations_to_payload(associated))
    try:
        response = await client.update_meeting(meeting_id, patch)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return _write_result_from("meeting", response)


@mcp.tool()
async def delete_note(note_id: int) -> WriteResult:
    """Delete a note via DELETE /v1/notes/{id}.

    Returns a ``WriteResult`` with the deleted id for trace.
    """
    try:
        await client.delete_note(note_id)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return WriteResult(kind="note", id=str(note_id))


# ---------------------------------------------------------------------------
# Assignment trio — candidate/job linkage
# ---------------------------------------------------------------------------


@mcp.tool()
async def assign_candidate(candidate_slug: str, job_slug: str) -> WriteResult:
    """Assign a candidate to a job via POST /v1/candidates/{slug}/assign.

    The target job is passed as a query param. No body is needed.
    """
    try:
        response = await client.assign_candidate(candidate_slug, job_slug)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return WriteResult(
        kind="assignment",
        id=str(response.get("candidate_slug") or candidate_slug),
        title=f"{candidate_slug} -> {job_slug}",
        url=response.get("shared_list_url"),
    )


@mcp.tool()
async def unassign_candidate(candidate_slug: str, job_slug: str) -> WriteResult:
    """Unassign a candidate from a job via POST /v1/candidates/{slug}/unassign."""
    try:
        await client.unassign_candidate(candidate_slug, job_slug)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return WriteResult(
        kind="assignment",
        id=str(candidate_slug),
        title=f"{candidate_slug} x {job_slug}",
    )


@mcp.tool()
async def update_hiring_stage(
    candidate_slug: str,
    job_slug: str,
    status_id: int,
    remark: str | None = None,
    stage_date: str | None = None,
    create_placement: bool | None = None,
) -> WriteResult:
    """Update a candidate's hiring stage for a specific job.

    POST /v1/candidates/{candidate_slug}/hiring-stages/{job_slug}. Use
    ``list_hiring_pipeline_stages`` to resolve ``status_id`` for the correct
    pipeline.
    """
    body = _build_payload({
        "status_id": status_id,
        "remark": remark,
        "stage_date": stage_date,
        "create_placement": create_placement,
    })
    try:
        response = await client.update_hiring_stage(candidate_slug, job_slug, body)
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return WriteResult(
        kind="assignment",
        id=str(response.get("candidate_slug") or candidate_slug),
        title=f"{candidate_slug} -> stage {status_id}",
    )


# ---------------------------------------------------------------------------
# File upload
# ---------------------------------------------------------------------------


@mcp.tool()
async def upload_file(
    file_url: str,
    related_to: EntityRef,
    folder: str = "Uploads",
) -> WriteResult:
    """Upload a file to Recruit CRM via POST /v1/files (multipart).

    ``file_url`` must be a publicly reachable URL — the Recruit CRM backend
    fetches the bytes itself. ``folder`` is the destination folder name (a
    sensible default is ``Uploads``). ``related_to`` anchors the file to a
    specific CRM entity.
    """
    try:
        response = await client.upload_file(
            file_url=file_url,
            related_to=related_to.id,
            related_to_type=related_to.kind,
            folder=folder,
        )
    except RecruitCrmError as exc:
        _reraise_as_tool_error(exc)
    return WriteResult(
        kind="file",
        id=response.get("file_link") or response.get("file_name") or "",
        title=response.get("file_name"),
        url=response.get("file_link"),
    )


@mcp.resource("recruitcrm://candidate/{candidate_id}/resume")
async def candidate_resume(candidate_id: str) -> str:
    """Get resume URL or text for a candidate."""
    data = await client.get_candidate(candidate_id)
    resume = data.get("resume")
    if isinstance(resume, dict):
        file_link = resume.get("file_link")
        if file_link:
            filename = resume.get("filename") or ""
            if filename:
                return f"Resume: {filename}\nURL: {file_link}"
            return f"Resume URL: {file_link}"
    return "No resume available for this candidate."


@mcp.resource("recruitcrm://job/{job_id}/description")
async def job_description(job_id: str) -> str:
    """Get the full description for a job."""
    data = await client.get_job(job_id)
    description = data.get("job_description_text") or ""
    title = data.get("name") or "Unknown"
    return f"# {title}\n\n{description}" if description else f"# {title}\n\nNo description available."


def main():
    mcp.run()


if __name__ == "__main__":
    main()
