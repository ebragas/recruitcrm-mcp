"""Recruit CRM MCP server."""

import os
from contextlib import asynccontextmanager
from importlib.metadata import version, PackageNotFoundError

from fastmcp import FastMCP

from recruit_crm_mcp import client

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
) -> list[dict]:
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
    return [_summarize_candidate(c) for c in results]


@mcp.tool()
async def get_candidate(candidate_id: str) -> dict:
    """Get full profile details for a specific candidate by slug or ID."""
    return await client.get_candidate(candidate_id)


@mcp.tool()
async def list_jobs(limit: int = 20) -> list[dict]:
    """List job requisitions without any filters.

    Returns jobs in reverse chronological order.
    Use search_jobs instead when you need to filter by status or other fields.
    """
    results = await client.list_jobs(limit=limit)
    return [_summarize_job(j) for j in results]


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
) -> list[dict]:
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
    return [_summarize_job(j) for j in results]


@mcp.tool()
async def get_job(job_id: str) -> dict:
    """Get full details for a specific job by slug or ID."""
    return await client.get_job(job_id)


@mcp.tool()
async def get_assigned_candidates(
    job_id: str,
    status_id: str | None = None,
    limit: int = 25,
) -> list[dict]:
    """Get candidates assigned to a specific job and their hiring stage.

    Returns candidate summaries with their current hiring status for the given job.
    Use status_id to filter by a specific hiring stage.
    """
    results = await client.get_assigned_candidates(
        job_slug=job_id,
        status_id=status_id,
        limit=limit,
    )
    summaries = []
    for item in results:
        summary = _summarize_candidate(item.get("candidate", {}))
        status = item.get("status") or {}
        summary["hiring_status"] = status.get("label")
        summaries.append(summary)
    return summaries


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
) -> list[dict]:
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
    return [_summarize_contact(c) for c in results]


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
) -> list[dict]:
    """Search for companies by name, date range, or owner.

    Provide at least one filter for targeted results. Filters are combined with AND logic.
    With no filters, returns a paginated list of recent companies.
    Date params use YYYY-MM-DD format.
    sort_by accepts 'createdon' or 'updatedon'. sort_order accepts 'asc' or 'desc'.
    Set exact_search=true for exact name matching (default is fuzzy/like matching).
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
    return [_summarize_company(c) for c in results]


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
) -> list[dict]:
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
    return [_summarize_meeting(m) for m in results]


@mcp.tool()
async def list_users() -> list[dict]:
    """List all team members/users.

    Useful for discovering owner IDs to use with the search_jobs owner_id filter.
    Returns id, name, email, and role for each user.
    """
    results = await client.list_users()
    return [_summarize_user(u) for u in results]


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


def _summarize_company(c: dict) -> dict:
    """Extract key fields from a company record for concise display."""
    return {
        "slug": c.get("slug"),
        "company_name": c.get("company_name"),
        "about_company": c.get("about_company"),
        "website": c.get("website"),
        "city": c.get("city"),
        "state": c.get("state"),
        "country": c.get("country"),
        "linkedin": c.get("linkedin"),
        "industry_id": c.get("industry_id"),
        "is_parent_company": c.get("is_parent_company"),
        "is_child_company": c.get("is_child_company"),
    }


def _summarize_meeting(m: dict) -> dict:
    """Extract key fields from a meeting record for concise display."""
    meeting_type = m.get("meeting_type")
    type_label = meeting_type.get("label") if isinstance(meeting_type, dict) else None
    return {
        "id": m.get("id"),
        "title": m.get("title"),
        "meeting_type": type_label,
        "status": m.get("status"),
        "start_date": m.get("start_date"),
        "end_date": m.get("end_date"),
        "all_day": m.get("all_day"),
        "address": m.get("address"),
        "related_to": m.get("related_to"),
        "related_to_type": m.get("related_to_type"),
        "owner": m.get("owner"),
    }


def _summarize_contact(c: dict) -> dict:
    """Extract key fields from a contact record for concise display."""
    return {
        "slug": c.get("slug"),
        "name": f"{c.get('first_name') or ''} {c.get('last_name') or ''}".strip(),
        "email": c.get("email"),
        "contact_number": c.get("contact_number"),
        "designation": c.get("designation"),
        "company_slug": c.get("company_slug"),
        "city": c.get("city"),
        "state": c.get("state"),
        "country": c.get("country"),
        "linkedin": c.get("linkedin"),
    }


def _summarize_candidate(c: dict) -> dict:
    """Extract key fields from a candidate record for concise display."""
    return {
        "slug": c.get("slug"),
        "name": f"{c.get('first_name') or ''} {c.get('last_name') or ''}".strip(),
        "email": c.get("email"),
        "position": c.get("position"),
        "company": c.get("current_organization"),
        "city": c.get("city"),
    }


_JOB_LOCATION_LABELS = {"0": "On-site", "1": "Remote", "2": "Hybrid"}


def _job_location_label(value: str | None) -> str:
    """Map job_location_type API values to human-readable labels."""
    if value is None:
        return ""
    return _JOB_LOCATION_LABELS.get(str(value), str(value))


def _summarize_job(j: dict) -> dict:
    """Extract key fields from a job record for concise display."""
    job_status = j.get("job_status")
    status_label = job_status.get("label") if isinstance(job_status, dict) else None
    return {
        "slug": j.get("slug"),
        "name": j.get("name"),
        "status": status_label,
        "city": j.get("city"),
        "country": j.get("country"),
        "job_type": j.get("job_type"),
        "job_location_type": _job_location_label(j.get("job_location_type")),
        "minimum_experience": j.get("minimum_experience"),
        "maximum_experience": j.get("maximum_experience"),
        "min_annual_salary": j.get("min_annual_salary"),
        "max_annual_salary": j.get("max_annual_salary"),
        "pay_rate": j.get("pay_rate"),
        "bill_rate": j.get("bill_rate"),
        "job_category": j.get("job_category"),
        "note_for_candidates": j.get("note_for_candidates"),
        "job_description_file": j.get("job_description_file"),
    }


def _summarize_user(u: dict) -> dict:
    """Extract key fields from a user record for concise display."""
    first = u.get("first_name") or ""
    last = u.get("last_name") or ""
    return {
        "id": u.get("id"),
        "name": f"{first} {last}".strip(),
        "email": u.get("email"),
        "role": u.get("role"),
    }


def main():
    mcp.run()


if __name__ == "__main__":
    main()
