"""MCP-layer tests for write tools.

Exercise the full FastMCP dispatch path (schema validation -> Pydantic arg
coercion -> tool body -> payload assembly) without hitting the live API.

These tests complement ``tests/integration/`` (which calls the ``client``
module directly) by catching tool-wrapper bugs — e.g. "server forgot to map
``EntityRef.kind`` to ``related_to_type``" or "``do_not_send_calendar_invites``
wasn't coerced to a string".

Pattern: monkeypatch the ``recruit_crm_mcp.client`` helper the tool delegates
to, invoke the tool via ``mcp_client.call_tool``, and assert on the payload
captured by the mock.
"""

from __future__ import annotations

import pytest

from recruit_crm_mcp import client
from recruit_crm_mcp.client import RecruitCrmError

pytestmark = [pytest.mark.anyio, pytest.mark.mcp]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_capture(return_value=None):
    """Return a (captured-dict, coroutine mock) pair for patching client fns.

    Usage:
        captured, mock = _make_capture({"id": 1})
        monkeypatch.setattr(client, "create_note", mock)
        ...
        assert captured["payload"] == {...}
    """
    captured: dict = {}
    rv = return_value if return_value is not None else {"id": 1}

    async def mock_fn(*args, **kwargs):
        # Support both positional (payload,) and (slug, patch) signatures.
        captured["args"] = args
        captured["kwargs"] = kwargs
        if len(args) == 1:
            captured["payload"] = args[0]
        elif len(args) >= 2:
            captured["slug_or_id"] = args[0]
            captured["payload"] = args[1]
        return rv

    return captured, mock_fn


# ---------------------------------------------------------------------------
# create_note — EntityRef.kind mapping, associations, None dropping
# ---------------------------------------------------------------------------


async def test_create_note_flattens_entity_ref(mcp_client, monkeypatch):
    """``EntityRef.kind`` must map to ``related_to_type`` in the client payload."""
    captured, mock = _make_capture({"id": 42, "title": "server-returned"})
    monkeypatch.setattr(client, "create_note", mock)

    result = await mcp_client.call_tool(
        "create_note",
        {
            "description": "Hello",
            "related_to": {"kind": "candidate", "id": "cand-1"},
        },
    )

    assert not result.is_error
    payload = captured["payload"]
    assert payload["description"] == "Hello"
    assert payload["related_to"] == "cand-1"
    assert payload["related_to_type"] == "candidate"
    assert "note_type_id" not in payload  # None-valued args must be dropped

    data = result.data
    assert data.kind == "note"
    assert data.id == "42"


async def test_create_note_flattens_associations(mcp_client, monkeypatch):
    """``Associations`` must flatten to ``associated_*`` comma-strings."""
    captured, mock = _make_capture()
    monkeypatch.setattr(client, "create_note", mock)

    result = await mcp_client.call_tool(
        "create_note",
        {
            "description": "multi-anchor",
            "related_to": {"kind": "contact", "id": "c-1"},
            "note_type_id": 7,
            "associated": {
                "candidates": ["cand-a", "cand-b"],
                "companies": ["co-1"],
                "contacts": [],
                "jobs": [],
                "deals": [],
            },
        },
    )

    assert not result.is_error
    payload = captured["payload"]
    assert payload["note_type_id"] == 7
    assert payload["associated_candidates"] == "cand-a,cand-b"
    assert payload["associated_companies"] == "co-1"
    # Empty lists are dropped entirely
    assert "associated_contacts" not in payload
    assert "associated_jobs" not in payload
    assert "associated_deals" not in payload


# ---------------------------------------------------------------------------
# log_meeting — EntityRef, attendees, associations, bool coercion
# ---------------------------------------------------------------------------


async def test_log_meeting_builds_full_payload(mcp_client, monkeypatch):
    captured, mock = _make_capture({"id": 100, "title": "Sync"})
    monkeypatch.setattr(client, "create_meeting", mock)

    result = await mcp_client.call_tool(
        "log_meeting",
        {
            "title": "Sync",
            "start_date": "2025-05-01T15:00:00Z",
            "end_date": "2025-05-01T15:30:00Z",
            "related_to": {"kind": "job", "id": "job-99"},
            "attendee_contacts": ["c-1", "c-2"],
            "attendee_candidates": ["cand-1"],
            "attendee_users": [7, 8],
            "meeting_type_id": 40014,
            "description": "desc",
            "address": "Zoom",
            "owner_id": 5,
            "associated": {
                "candidates": ["cand-x", "cand-y"],
                "companies": [],
                "contacts": [],
                "jobs": [],
                "deals": ["deal-1"],
            },
            "do_not_send_calendar_invites": True,
        },
    )

    assert not result.is_error
    payload = captured["payload"]
    # EntityRef mapping
    assert payload["related_to"] == "job-99"
    assert payload["related_to_type"] == "job"
    # Attendee lists -> comma strings (mixed types ok)
    assert payload["attendee_contacts"] == "c-1,c-2"
    assert payload["attendee_candidates"] == "cand-1"
    assert payload["attendee_users"] == "7,8"
    # Associations flatten, empties dropped
    assert payload["associated_candidates"] == "cand-x,cand-y"
    assert payload["associated_deals"] == "deal-1"
    assert "associated_companies" not in payload
    assert "associated_contacts" not in payload
    assert "associated_jobs" not in payload
    # Bool coerced to string "1"/"0" (API rejects JSON `false`)
    assert payload["do_not_send_calendar_invites"] == "1"
    # Other scalars forwarded
    assert payload["meeting_type_id"] == 40014
    assert payload["owner_id"] == 5
    assert payload["address"] == "Zoom"
    assert payload["description"] == "desc"


async def test_log_meeting_bool_false_coerces_to_zero(mcp_client, monkeypatch):
    captured, mock = _make_capture()
    monkeypatch.setattr(client, "create_meeting", mock)

    result = await mcp_client.call_tool(
        "log_meeting",
        {
            "title": "Sync",
            "start_date": "2025-05-01T15:00:00Z",
            "end_date": "2025-05-01T15:30:00Z",
            "related_to": {"kind": "candidate", "id": "cand-1"},
            "do_not_send_calendar_invites": False,
        },
    )

    assert not result.is_error
    assert captured["payload"]["do_not_send_calendar_invites"] == "0"


async def test_log_meeting_drops_empty_attendee_lists(mcp_client, monkeypatch):
    """Default empty lists must NOT appear in the payload."""
    captured, mock = _make_capture()
    monkeypatch.setattr(client, "create_meeting", mock)

    result = await mcp_client.call_tool(
        "log_meeting",
        {
            "title": "Sync",
            "start_date": "2025-05-01T15:00:00Z",
            "end_date": "2025-05-01T15:30:00Z",
            "related_to": {"kind": "company", "id": "co-1"},
        },
    )

    assert not result.is_error
    payload = captured["payload"]
    assert "attendee_contacts" not in payload
    assert "attendee_candidates" not in payload
    assert "attendee_users" not in payload
    # Default bool=True still emitted
    assert payload["do_not_send_calendar_invites"] == "1"


# ---------------------------------------------------------------------------
# create_task — optional related_to, default reminder, None dropping
# ---------------------------------------------------------------------------


async def test_create_task_without_related_to_omits_keys(mcp_client, monkeypatch):
    """When ``related_to`` is omitted, payload must NOT contain the mapping keys."""
    captured, mock = _make_capture({"id": 55, "title": "Call"})
    monkeypatch.setattr(client, "create_task", mock)

    result = await mcp_client.call_tool(
        "create_task",
        {"title": "Call", "start_date": "2025-05-01T10:00:00Z"},
    )

    assert not result.is_error
    payload = captured["payload"]
    assert payload["title"] == "Call"
    assert payload["reminder"] == 1440  # default "one day before"
    assert "related_to" not in payload
    assert "related_to_type" not in payload
    # None values dropped
    assert "description" not in payload
    assert "task_type_id" not in payload
    assert "owner_id" not in payload


async def test_create_task_with_related_to_and_task_type(mcp_client, monkeypatch):
    captured, mock = _make_capture()
    monkeypatch.setattr(client, "create_task", mock)

    result = await mcp_client.call_tool(
        "create_task",
        {
            "title": "Call",
            "start_date": "2025-05-01T10:00:00Z",
            "reminder": 60,
            "task_type_id": 1,
            "owner_id": 7,
            "description": "desc",
            "related_to": {"kind": "contact", "id": "c-1"},
        },
    )

    assert not result.is_error
    payload = captured["payload"]
    assert payload["related_to"] == "c-1"
    assert payload["related_to_type"] == "contact"
    assert payload["task_type_id"] == 1
    assert payload["reminder"] == 60


# ---------------------------------------------------------------------------
# update_task — None dropping (status field intentionally NOT exposed; see
# CLAUDE.md gotcha: API silently ignores task status writes)
# ---------------------------------------------------------------------------


async def test_update_task_drops_none_and_forwards_provided(mcp_client, monkeypatch):
    captured, mock = _make_capture({"id": 42, "title": "updated"})
    monkeypatch.setattr(client, "update_task", mock)

    result = await mcp_client.call_tool(
        "update_task",
        {"task_id": 42, "title": "new-title", "task_type_id": 2},
    )

    assert not result.is_error
    assert captured["slug_or_id"] == 42
    patch = captured["payload"]
    assert patch == {"title": "new-title", "task_type_id": 2}


# ---------------------------------------------------------------------------
# update_meeting — None vs False/True for do_not_send_calendar_invites
# ---------------------------------------------------------------------------


async def test_update_meeting_calendar_invite_tri_state(mcp_client, monkeypatch):
    """``None`` -> omitted; ``True`` -> ``"1"``; ``False`` -> ``"0"``."""
    captured, mock = _make_capture()
    monkeypatch.setattr(client, "update_meeting", mock)

    # Case 1: do_not_send_calendar_invites omitted -> not in payload
    result = await mcp_client.call_tool(
        "update_meeting", {"meeting_id": 9, "title": "renamed"}
    )
    assert not result.is_error
    assert "do_not_send_calendar_invites" not in captured["payload"]

    # Case 2: True -> "1"
    result = await mcp_client.call_tool(
        "update_meeting",
        {"meeting_id": 9, "do_not_send_calendar_invites": True},
    )
    assert not result.is_error
    assert captured["payload"]["do_not_send_calendar_invites"] == "1"

    # Case 3: False -> "0"
    result = await mcp_client.call_tool(
        "update_meeting",
        {"meeting_id": 9, "do_not_send_calendar_invites": False},
    )
    assert not result.is_error
    assert captured["payload"]["do_not_send_calendar_invites"] == "0"


async def test_update_meeting_related_to_optional(mcp_client, monkeypatch):
    """Omitting ``related_to`` must not leave orphan keys in the patch."""
    captured, mock = _make_capture()
    monkeypatch.setattr(client, "update_meeting", mock)

    result = await mcp_client.call_tool(
        "update_meeting", {"meeting_id": 9, "address": "Zoom"}
    )

    assert not result.is_error
    payload = captured["payload"]
    assert payload == {"address": "Zoom"}


# ---------------------------------------------------------------------------
# Entity create/update — custom_fields flatten via model_dump, None dropped
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "tool_name,client_fn,required_args",
    [
        (
            "create_company",
            "create_company",
            {"company_name": "Acme Corp"},
        ),
        (
            "create_contact",
            "create_contact",
            {"first_name": "Ada", "last_name": "Lovelace"},
        ),
        (
            "create_job",
            "create_job",
            {
                "name": "SWE",
                "company_slug": "acme",
                "contact_slug": "hm-1",
                "number_of_openings": 1,
                "currency_id": 1,
                "enable_job_application_form": 1,
                "job_description_text": "<p>desc</p>",
            },
        ),
        (
            "create_candidate",
            "create_candidate",
            {"first_name": "Grace"},
        ),
    ],
)
async def test_create_entity_forwards_custom_fields(
    mcp_client, monkeypatch, tool_name, client_fn, required_args
):
    """Custom fields must flatten via ``model_dump()`` and ride on the create body."""
    captured, mock = _make_capture({"slug": "new-slug", "id": 1})
    monkeypatch.setattr(client, client_fn, mock)

    args = dict(required_args)
    args["custom_fields"] = [
        {"field_id": 100, "value": "alpha"},
        {"field_id": 101, "value": "beta"},
    ]

    result = await mcp_client.call_tool(tool_name, args)

    assert not result.is_error, getattr(result, "content", None)
    payload = captured["payload"]
    assert payload["custom_fields"] == [
        {"field_id": 100, "value": "alpha"},
        {"field_id": 101, "value": "beta"},
    ]
    # Required args must appear in payload
    for key, expected in required_args.items():
        assert payload[key] == expected


@pytest.mark.parametrize(
    "tool_name,client_fn,slug_arg,slug_value",
    [
        ("update_company", "update_company", "slug", "acme"),
        ("update_contact", "update_contact", "slug", "ada"),
        ("update_job", "update_job", "slug", "job-1"),
        ("update_candidate", "update_candidate", "slug", "grace"),
    ],
)
async def test_update_entity_drops_none_fields(
    mcp_client, monkeypatch, tool_name, client_fn, slug_arg, slug_value
):
    """Update patches must only contain fields the caller actually set."""
    captured, mock = _make_capture({"slug": slug_value})
    monkeypatch.setattr(client, client_fn, mock)

    # Only provide custom_fields — no standard fields touched.
    result = await mcp_client.call_tool(
        tool_name,
        {slug_arg: slug_value, "custom_fields": [{"field_id": 9, "value": "x"}]},
    )

    assert not result.is_error, getattr(result, "content", None)
    assert captured["slug_or_id"] == slug_value
    patch = captured["payload"]
    assert patch == {"custom_fields": [{"field_id": 9, "value": "x"}]}


# ---------------------------------------------------------------------------
# set_*_custom_fields — wrappers delegate and only touch custom_fields
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "tool_name,client_fn,slug_value",
    [
        ("set_company_custom_fields", "update_company", "acme"),
        ("set_contact_custom_fields", "update_contact", "ada"),
        ("set_job_custom_fields", "update_job", "job-1"),
        ("set_candidate_custom_fields", "update_candidate", "grace"),
    ],
)
async def test_set_custom_fields_wrapper_sends_only_custom_fields(
    mcp_client, monkeypatch, tool_name, client_fn, slug_value
):
    captured, mock = _make_capture({"slug": slug_value})
    monkeypatch.setattr(client, client_fn, mock)

    result = await mcp_client.call_tool(
        tool_name,
        {
            "slug": slug_value,
            "fields": [{"field_id": 50, "value": "v"}],
        },
    )

    assert not result.is_error, getattr(result, "content", None)
    assert captured["slug_or_id"] == slug_value
    patch = captured["payload"]
    # Exactly one key — no accidental standard-field bleed.
    assert set(patch.keys()) == {"custom_fields"}
    assert patch["custom_fields"] == [{"field_id": 50, "value": "v"}]


# ---------------------------------------------------------------------------
# Assignment tools
# ---------------------------------------------------------------------------


async def test_assign_candidate_dispatches_to_client(mcp_client, monkeypatch):
    captured, mock = _make_capture(
        {"candidate_slug": "grace", "shared_list_url": "https://x"}
    )
    monkeypatch.setattr(client, "assign_candidate", mock)

    result = await mcp_client.call_tool(
        "assign_candidate",
        {"candidate_slug": "grace", "job_slug": "job-1"},
    )

    assert not result.is_error
    assert captured["args"] == ("grace", "job-1")
    data = result.data
    assert data.kind == "assignment"
    assert data.id == "grace"
    assert data.url == "https://x"


async def test_unassign_candidate_dispatches_to_client(mcp_client, monkeypatch):
    captured, mock = _make_capture({})
    monkeypatch.setattr(client, "unassign_candidate", mock)

    result = await mcp_client.call_tool(
        "unassign_candidate",
        {"candidate_slug": "grace", "job_slug": "job-1"},
    )

    assert not result.is_error
    assert captured["args"] == ("grace", "job-1")
    data = result.data
    assert data.kind == "assignment"
    assert data.id == "grace"
    assert "grace" in (data.title or "")
    assert "job-1" in (data.title or "")


async def test_update_hiring_stage_builds_body(mcp_client, monkeypatch):
    captured, mock = _make_capture({"candidate_slug": "grace"})
    monkeypatch.setattr(client, "update_hiring_stage", mock)

    result = await mcp_client.call_tool(
        "update_hiring_stage",
        {
            "candidate_slug": "grace",
            "job_slug": "job-1",
            "status_id": 5,
            "remark": "moved to interview",
        },
    )

    assert not result.is_error
    # client.update_hiring_stage(candidate_slug, job_slug, body)
    args = captured["args"]
    assert args[0] == "grace"
    assert args[1] == "job-1"
    body = args[2]
    assert body == {"status_id": 5, "remark": "moved to interview"}


# ---------------------------------------------------------------------------
# delete_note
# ---------------------------------------------------------------------------


async def test_delete_note_dispatches_and_returns_write_result(mcp_client, monkeypatch):
    captured: dict = {}

    async def mock_delete(note_id):
        captured["note_id"] = note_id
        return None

    monkeypatch.setattr(client, "delete_note", mock_delete)

    result = await mcp_client.call_tool("delete_note", {"note_id": 777})

    assert not result.is_error
    assert captured["note_id"] == 777
    data = result.data
    assert data.kind == "note"
    assert data.id == "777"


# ---------------------------------------------------------------------------
# upload_file — multipart wrapper
# ---------------------------------------------------------------------------


async def test_upload_file_forwards_entity_ref_and_folder(mcp_client, monkeypatch):
    captured: dict = {}

    async def mock_upload(*, file_url, related_to, related_to_type, folder):
        captured.update(
            file_url=file_url,
            related_to=related_to,
            related_to_type=related_to_type,
            folder=folder,
        )
        return {"file_name": "resume.pdf", "file_link": "https://x/resume.pdf"}

    monkeypatch.setattr(client, "upload_file", mock_upload)

    result = await mcp_client.call_tool(
        "upload_file",
        {
            "file_url": "https://example.com/resume.pdf",
            "related_to": {"kind": "candidate", "id": "grace"},
            "folder": "Resumes",
        },
    )

    assert not result.is_error
    assert captured["file_url"] == "https://example.com/resume.pdf"
    assert captured["related_to"] == "grace"
    assert captured["related_to_type"] == "candidate"
    assert captured["folder"] == "Resumes"
    data = result.data
    assert data.kind == "file"
    assert data.url == "https://x/resume.pdf"


# ---------------------------------------------------------------------------
# Error surfacing — RecruitCrmError -> ToolError via _reraise_as_tool_error
# ---------------------------------------------------------------------------


async def test_client_error_surfaces_as_tool_error(mcp_client, monkeypatch):
    """Validate the end-to-end error wiring: ``RecruitCrmError`` body turns
    into a ``ToolError`` whose message flattens field validation messages
    cleanly — not ``str(dict)`` gibberish.

    FastMCP's in-process transport re-raises ``ToolError`` on the client side
    rather than returning ``is_error=True`` (that shape is for wire transports).
    """
    from fastmcp.exceptions import ToolError

    async def mock_create_note(payload):
        raise RecruitCrmError(
            status=422,
            body={"description": ["The description field is required."]},
            method="POST",
            path="/notes",
        )

    monkeypatch.setattr(client, "create_note", mock_create_note)

    with pytest.raises(ToolError) as excinfo:
        await mcp_client.call_tool(
            "create_note",
            {
                "description": "x",  # passes schema; server-side raises
                "related_to": {"kind": "candidate", "id": "grace"},
            },
        )

    msg = str(excinfo.value)
    assert "422" in msg
    assert "description" in msg
    # The dict body must be flattened — not a raw Python repr.
    assert "{" not in msg, f"body dict leaked into message: {msg!r}"
    assert "The description field is required." in msg
