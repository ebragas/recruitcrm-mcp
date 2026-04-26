"""Orphan-sweep helper for integration tests.

Searches each top-level entity type for the canonical ``MCP-Test-`` prefix
and deletes matches. Per-entity errors are caught and logged so one bad
delete doesn't abort the whole sweep. Returns a dict of counts per entity
type for the session-end summary.

Run standalone: ``uv run python -m tests.integration._sweep``
"""
from __future__ import annotations

import asyncio
import logging

from recruit_crm_mcp import client

logger = logging.getLogger(__name__)

PREFIX = "MCP-Test-"
SEARCH_LIMIT = 100


def _starts_with_prefix(value: str | None) -> bool:
    return isinstance(value, str) and value.startswith(PREFIX)


async def _delete(path: str, kind: str, ident: str, counts: dict[str, int]) -> None:
    try:
        await client.delete(path)
        counts[kind] += 1
    except Exception as exc:
        counts["errors"] += 1
        logger.warning("Sweep failed to delete %s %s: %s", kind, ident, exc)


async def _sweep_candidates(counts: dict[str, int]) -> None:
    try:
        results = await client.search_candidates(first_name=PREFIX, limit=SEARCH_LIMIT)
    except Exception as exc:
        counts["errors"] += 1
        logger.warning("Sweep failed to search candidates: %s", exc)
        return
    for cand in results:
        if _starts_with_prefix(cand.get("first_name")):
            slug = cand.get("slug")
            if slug:
                await _delete(f"/candidates/{slug}", "candidates", slug, counts)


async def _sweep_contacts(counts: dict[str, int]) -> None:
    try:
        results = await client.search_contacts(first_name=PREFIX, limit=SEARCH_LIMIT)
    except Exception as exc:
        counts["errors"] += 1
        logger.warning("Sweep failed to search contacts: %s", exc)
        return
    for contact in results:
        if _starts_with_prefix(contact.get("first_name")):
            slug = contact.get("slug")
            if slug:
                await _delete(f"/contacts/{slug}", "contacts", slug, counts)


async def _sweep_companies(counts: dict[str, int]) -> None:
    try:
        results = await client.search_companies(
            company_name=PREFIX, exact_search=False, limit=SEARCH_LIMIT
        )
    except Exception as exc:
        counts["errors"] += 1
        logger.warning("Sweep failed to search companies: %s", exc)
        return
    for company in results:
        if _starts_with_prefix(company.get("company_name")):
            slug = company.get("slug")
            if slug:
                await _delete(f"/companies/{slug}", "companies", slug, counts)


async def _sweep_jobs(counts: dict[str, int]) -> None:
    # /jobs/search has no name filter (per CLAUDE.md), so list and filter
    # client-side. SEARCH_LIMIT caps each sweep pass.
    try:
        results = await client.list_jobs(limit=SEARCH_LIMIT)
    except Exception as exc:
        counts["errors"] += 1
        logger.warning("Sweep failed to list jobs: %s", exc)
        return
    for job in results:
        if _starts_with_prefix(job.get("name")):
            slug = job.get("slug")
            if slug:
                await _delete(f"/jobs/{slug}", "jobs", slug, counts)


async def _sweep_tasks(counts: dict[str, int]) -> None:
    try:
        results = await client.search_tasks(title=PREFIX, limit=SEARCH_LIMIT)
    except Exception as exc:
        counts["errors"] += 1
        logger.warning("Sweep failed to search tasks: %s", exc)
        return
    for task in results:
        if _starts_with_prefix(task.get("title")):
            tid = task.get("id")
            if tid is not None:
                await _delete(f"/tasks/{tid}", "tasks", str(tid), counts)


async def _sweep_meetings(counts: dict[str, int]) -> None:
    try:
        results = await client.search_meetings(title=PREFIX, limit=SEARCH_LIMIT)
    except Exception as exc:
        counts["errors"] += 1
        logger.warning("Sweep failed to search meetings: %s", exc)
        return
    for meeting in results:
        if _starts_with_prefix(meeting.get("title")):
            mid = meeting.get("id")
            if mid is not None:
                await _delete(f"/meetings/{mid}", "meetings", str(mid), counts)


async def _sweep_notes(counts: dict[str, int]) -> None:
    # /notes/search has no description filter (per CLAUDE.md), so list and
    # filter client-side. Notes are typically cascade-deleted with their
    # parent candidate/contact/job — this is a backstop.
    try:
        results = await client.search_notes(limit=SEARCH_LIMIT)
    except Exception as exc:
        counts["errors"] += 1
        logger.warning("Sweep failed to list notes: %s", exc)
        return
    for note in results:
        if _starts_with_prefix(note.get("description")):
            nid = note.get("id")
            if nid is not None:
                try:
                    await client.delete_note(nid)
                    counts["notes"] += 1
                except Exception as exc:
                    counts["errors"] += 1
                    logger.warning("Sweep failed to delete note %s: %s", nid, exc)


async def sweep_orphans() -> dict[str, int]:
    """Sweep all integration-test orphans matching the canonical prefix.

    Returns a per-type count dict including an ``errors`` tally.
    """
    counts = {
        "candidates": 0,
        "contacts": 0,
        "companies": 0,
        "jobs": 0,
        "tasks": 0,
        "meetings": 0,
        "notes": 0,
        "errors": 0,
    }
    # Order matters: sweep child entities (notes/tasks/meetings) first so any
    # explicit deletes succeed before parents are removed; then top-level
    # entities. The API likely cascades on parent delete, but ordering avoids
    # relying on that contract.
    await _sweep_notes(counts)
    await _sweep_tasks(counts)
    await _sweep_meetings(counts)
    await _sweep_jobs(counts)
    await _sweep_candidates(counts)
    await _sweep_contacts(counts)
    await _sweep_companies(counts)
    return counts


async def _main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    client.init_client()
    try:
        counts = await sweep_orphans()
        print(f"[integration sweep] {counts}")
    finally:
        await client.aclose_client()


if __name__ == "__main__":
    asyncio.run(_main())
