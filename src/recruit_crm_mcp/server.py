"""Recruit CRM MCP server."""

import os
from importlib.metadata import version, PackageNotFoundError

from fastmcp import FastMCP

from recruit_crm_mcp import client

try:
    __version__ = version("recruit-crm-mcp")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

mcp = FastMCP("Recruit CRM")


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
    query: str | None = None,
    email: str | None = None,
    city: str | None = None,
    job_title: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """Search for candidates by free-text query, email, city, or job title.

    Use `query` for general search, or filter by specific fields.
    Returns a list of matching candidate summaries.
    """
    results = await client.search_candidates(
        query=query, email=email, city=city, job_title=job_title, limit=limit
    )
    return [_summarize_candidate(c) for c in results]


@mcp.tool()
async def get_candidate(candidate_id: str) -> dict:
    """Get full profile details for a specific candidate by slug or ID."""
    return await client.get_candidate(candidate_id)


@mcp.tool()
async def list_jobs(status: str | None = None, limit: int = 20) -> list[dict]:
    """List job requisitions, optionally filtered by status (e.g. 'Open', 'Closed').

    Returns a list of job summaries.
    """
    results = await client.list_jobs(status=status, limit=limit)
    return [_summarize_job(j) for j in results]


@mcp.tool()
async def get_job(job_id: str) -> dict:
    """Get full details for a specific job by slug or ID."""
    return await client.get_job(job_id)


@mcp.resource("recruitcrm://candidate/{candidate_id}/resume")
async def candidate_resume(candidate_id: str) -> str:
    """Get resume URL or text for a candidate."""
    data = await client.get_candidate(candidate_id)
    resume = data.get("resume")
    if isinstance(resume, dict) and resume.get("file_link"):
        return f"Resume: {resume['filename']}\nURL: {resume['file_link']}"
    return "No resume available for this candidate."


@mcp.resource("recruitcrm://job/{job_id}/description")
async def job_description(job_id: str) -> str:
    """Get the full description for a job."""
    data = await client.get_job(job_id)
    description = data.get("job_description_text") or ""
    title = data.get("name") or "Unknown"
    return f"# {title}\n\n{description}" if description else f"# {title}\n\nNo description available."


def _summarize_candidate(c: dict) -> dict:
    """Extract key fields from a candidate record for concise display."""
    return {
        "slug": c.get("slug"),
        "name": f"{c.get('first_name', '')} {c.get('last_name', '')}".strip(),
        "email": c.get("email"),
        "position": c.get("position"),
        "company": c.get("current_organization"),
        "city": c.get("city"),
    }


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
    }


def main():
    mcp.run()


if __name__ == "__main__":
    main()
