"""Live-API end-to-end tests for write tools dispatched through FastMCP.

These tests gate pre-deploy confidence: "the wheel on PyPI, run through
``uvx``, actually creates a note on a real Recruit CRM tenant." Each test
exercises the full stack:

    MCP schema validation → arg coercion → tool body → client HTTP call
        → live Recruit CRM API → response → WriteResult serialization

Anchors use the throwaway fixtures in ``tests/mcp/conftest.py`` (candidate,
contact) so writes never touch real tenant records. Every create is paired
with a delete in ``try/finally`` so a crash mid-test doesn't leak records.

Rate limit: Recruit CRM allows 60 req/min; the full file issues <20 calls.
"""

from __future__ import annotations

import pytest

from recruit_crm_mcp import client

pytestmark = [pytest.mark.anyio, pytest.mark.mcp, pytest.mark.mcp_live]


def _write_result_dict(result) -> dict:
    """Coerce ``result.data`` (WriteResult dataclass) into a plain dict.

    FastMCP hydrates structured returns into a dataclass when an output schema
    is present (``WriteResult`` here). ``structured_content`` is the raw JSON
    dict — use it for uniform dict access across tests.
    """
    sc = getattr(result, "structured_content", None)
    if isinstance(sc, dict):
        return sc
    # Fallback — dataclass → __dict__ (no nested hydration to worry about for WriteResult).
    data = result.data
    return data if isinstance(data, dict) else {**data.__dict__}


async def test_create_note_live(mcp_client, test_candidate):
    """``create_note`` round-trips via FastMCP dispatch + live API + WriteResult."""
    description = "MCP live-test note"
    result = await mcp_client.call_tool(
        "create_note",
        {
            "description": description,
            "related_to": {"kind": "candidate", "id": test_candidate},
        },
    )
    assert result.is_error is False, f"create_note errored: {result.content!r}"
    data = _write_result_dict(result)
    assert data["kind"] == "note"
    assert isinstance(data["id"], str) and data["id"], "expected non-empty id string"

    note_id = int(data["id"])
    try:
        fetched = await mcp_client.call_tool("get_note", {"note_id": note_id})
        assert fetched.is_error is False, f"get_note errored: {fetched.content!r}"
        # ``get_note`` is typed as ``dict`` in server.py so ``data`` is already a dict.
        fetched_data = fetched.data
        assert fetched_data["id"] == note_id
        assert fetched_data.get("description") == description
        assert fetched_data.get("related_to") == test_candidate
        assert fetched_data.get("related_to_type") == "candidate"
    finally:
        # delete_note is registered as an MCP tool — clean up through the same layer.
        await mcp_client.call_tool("delete_note", {"note_id": note_id})


async def test_log_meeting_live_with_attendees(mcp_client, test_candidate):
    """``log_meeting`` with candidate attendee round-trips through live API.

    Uses future dates + ``do_not_send_calendar_invites=True`` so no real
    calendar invites fire on the tenant.
    """
    title = "MCP live-test meeting"
    result = await mcp_client.call_tool(
        "log_meeting",
        {
            "title": title,
            "start_date": "2030-01-01T09:00:00Z",
            "end_date": "2030-01-01T10:00:00Z",
            "related_to": {"kind": "candidate", "id": test_candidate},
            "attendee_candidates": [test_candidate],
            "do_not_send_calendar_invites": True,
            "reminder": -1,
        },
    )
    assert result.is_error is False, f"log_meeting errored: {result.content!r}"
    data = _write_result_dict(result)
    assert data["kind"] == "meeting"
    assert isinstance(data["id"], str) and data["id"], "expected non-empty id string"

    meeting_id = int(data["id"])
    try:
        fetched = await mcp_client.call_tool("get_meeting", {"meeting_id": meeting_id})
        assert fetched.is_error is False, f"get_meeting errored: {fetched.content!r}"
        fetched_data = fetched.data
        assert fetched_data["id"] == meeting_id
        assert fetched_data.get("title") == title

        # Attendee round-trip: the live API does NOT echo ``attendee_candidates``
        # on GET (it's None). Instead it exposes a separate ``attendees`` list
        # of dicts with ``attendee_id``/``attendee_type``/``display_name`` keys
        # (see tests/integration/test_write_variants.py for the contract).
        attendees = fetched_data.get("attendees") or []
        assert isinstance(attendees, list), (
            f"expected 'attendees' list, got {type(attendees).__name__}: {attendees!r}"
        )
        attendee_ids = [a.get("attendee_id") for a in attendees if isinstance(a, dict)]
        assert test_candidate in attendee_ids, (
            f"expected candidate slug {test_candidate!r} in attendees, got {attendees!r}"
        )
    finally:
        # No ``delete_meeting`` MCP tool — fall back to the raw client.
        try:
            await client.delete(f"/meetings/{meeting_id}")
        except Exception:
            pass


async def test_create_task_and_update_live(mcp_client, test_candidate):
    """``create_task`` + ``update_task`` round-trip end-to-end through FastMCP."""
    original_title = "MCP live-test task"
    created = await mcp_client.call_tool(
        "create_task",
        {
            "title": original_title,
            "start_date": "2030-01-01T09:00:00Z",
            "description": "original description",
            "reminder": -1,
            "related_to": {"kind": "candidate", "id": test_candidate},
        },
    )
    assert created.is_error is False, f"create_task errored: {created.content!r}"
    created_data = _write_result_dict(created)
    assert created_data["kind"] == "task"
    task_id = int(created_data["id"])

    try:
        updated = await mcp_client.call_tool(
            "update_task",
            {"task_id": task_id, "description": "patched description"},
        )
        assert updated.is_error is False, f"update_task errored: {updated.content!r}"
        assert _write_result_dict(updated)["kind"] == "task"

        fetched = await mcp_client.call_tool("get_task", {"task_id": task_id})
        assert fetched.is_error is False, f"get_task errored: {fetched.content!r}"
        fetched_data = fetched.data
        assert fetched_data["id"] == task_id
        assert fetched_data.get("title") == original_title, (
            f"title should be preserved across update, got {fetched_data.get('title')!r}"
        )
        assert fetched_data.get("description") == "patched description", (
            f"description should be updated, got {fetched_data.get('description')!r}"
        )
    finally:
        # No ``delete_task`` MCP tool — fall back to the raw client.
        try:
            await client.delete(f"/tasks/{task_id}")
        except Exception:
            pass


async def test_update_contact_live(mcp_client, test_contact):
    """``update_contact`` round-trips a single-field change through FastMCP + live API.

    The ``test_contact`` fixture handles teardown.
    """
    new_city = "MCP-City-Test"
    result = await mcp_client.call_tool(
        "update_contact",
        {"slug": test_contact, "city": new_city},
    )
    assert result.is_error is False, f"update_contact errored: {result.content!r}"
    assert _write_result_dict(result)["kind"] == "contact"

    fetched = await mcp_client.call_tool("get_contact", {"contact_slug": test_contact})
    assert fetched.is_error is False, f"get_contact errored: {fetched.content!r}"
    assert fetched.data.get("city") == new_city, (
        f"expected city={new_city!r}, got {fetched.data.get('city')!r}"
    )


async def test_create_note_rejects_invalid_related_to_type_live(mcp_client):
    """Rejection guard — live API rejects unknown candidate slugs via RecruitCrmError.

    Ensures ``_reraise_as_tool_error`` (in ``server.py``) surfaces API-side
    validation cleanly to the MCP client: the error must be routed through
    ``CallToolResult.is_error`` with a useful text body (status code + field hint).
    """
    result = await mcp_client.call_tool(
        "create_note",
        {
            "description": "MCP live-test invalid related_to",
            "related_to": {"kind": "candidate", "id": "nonexistent-slug-xxx"},
        },
        raise_on_error=False,
    )
    assert result.is_error is True, (
        f"expected isError=True for invalid slug, got isError=False with data={result.data!r}"
    )
    # The error message should include status code info (e.g. "422" or "404") so
    # the LLM caller can distinguish validation from auth failures.
    content_text = "".join(
        getattr(block, "text", "") for block in (result.content or [])
    )
    assert content_text, "expected an error message in result.content"
    # Recruit CRM typically returns 422 for invalid related_to slugs; accept any 4xx.
    assert any(code in content_text for code in ("400", "404", "422")), (
        f"expected a 4xx status code in error message, got: {content_text!r}"
    )
