"""Integration tests probing the live API's tolerance for the
``do_not_send_calendar_invites`` flag on POST /v1/meetings.

The Recruit CRM docs (docs/api-reference/creates-a-new-meeting.md) describe
the field as a string ("1"/"0"). Our MCP server tools (log_meeting,
update_meeting) now serialize Python bools to those strings before sending,
because the live API rejects JSON ``false`` with 422. These tests intentionally
exercise the raw client payloads — not the server tools — to lock in what
the live API accepts so we don't silently misbehave and accidentally spam
real calendar invites.

All meetings are scheduled far in the future (2030) so they don't clutter
current schedules, and use ``@example.invalid`` domains for any external-looking
attendees so even an unintended invite is undeliverable.
"""

import pytest

from recruit_crm_mcp import client

from tests.integration.conftest import _test_label

pytestmark = [pytest.mark.anyio, pytest.mark.integration]


async def test_do_not_send_as_python_bool_accepted(test_candidate):
    """Submitting ``do_not_send_calendar_invites=True`` (Python bool) should
    be accepted by the API and round-trip as a truthy value."""
    payload = {
        "title": _test_label("InviteBoolTrue"),
        "start_date": "2030-01-01T09:00:00Z",
        "end_date": "2030-01-01T10:00:00Z",
        "reminder": -1,
        "related_to": test_candidate,
        "related_to_type": "candidate",
        "attendee_candidates": test_candidate,
        "do_not_send_calendar_invites": True,
    }
    created = await client.create_meeting(payload)
    meeting_id = created.get("id")
    assert meeting_id, f"Expected id in create-meeting response, got {created!r}"
    try:
        fetched = await client.get_meeting(meeting_id)
        assert fetched["id"] == meeting_id
        flag = fetched.get("do_not_send_calendar_invites")
        assert flag in (True, 1, "1", "true"), (
            f"Expected do_not_send_calendar_invites truthy, got {flag!r}"
        )
    finally:
        await client.delete(f"/meetings/{meeting_id}")


async def test_do_not_send_as_string_one_accepted(test_candidate):
    """Submitting ``do_not_send_calendar_invites="1"`` (string per docs) should
    also be accepted by the API and round-trip as a truthy value."""
    payload = {
        "title": _test_label("InviteStrOne"),
        "start_date": "2030-01-01T09:00:00Z",
        "end_date": "2030-01-01T10:00:00Z",
        "reminder": -1,
        "related_to": test_candidate,
        "related_to_type": "candidate",
        "attendee_candidates": test_candidate,
        "do_not_send_calendar_invites": "1",
    }
    created = await client.create_meeting(payload)
    meeting_id = created.get("id")
    assert meeting_id, f"Expected id in create-meeting response, got {created!r}"
    try:
        fetched = await client.get_meeting(meeting_id)
        assert fetched["id"] == meeting_id
        flag = fetched.get("do_not_send_calendar_invites")
        assert flag in (True, 1, "1", "true"), (
            f"Expected do_not_send_calendar_invites truthy, got {flag!r}"
        )
    finally:
        await client.delete(f"/meetings/{meeting_id}")


async def test_do_not_send_python_false_is_rejected(test_candidate):
    """Rejection guard: the live API returns 422 for JSON ``false``.

    This is a known Laravel-validator quirk — ``true`` coerces to 1, but
    ``false`` fails the ``in:0,1`` rule. Server code therefore serializes
    Python bools to ``"1"``/``"0"`` strings before POSTing. If this test
    ever starts passing, the API has changed and the server-side coercion
    may be removable; update both simultaneously.
    """
    from recruit_crm_mcp.client import RecruitCrmError

    payload = {
        "title": _test_label("InviteBoolFalse"),
        "start_date": "2030-01-01T09:00:00Z",
        "end_date": "2030-01-01T10:00:00Z",
        "reminder": -1,
        "related_to": test_candidate,
        "related_to_type": "candidate",
        "attendee_candidates": test_candidate,
        "do_not_send_calendar_invites": False,
    }
    with pytest.raises(RecruitCrmError) as exc_info:
        await client.create_meeting(payload)
    assert exc_info.value.status == 422
    body = exc_info.value.body
    assert isinstance(body, dict) and "do_not_send_calendar_invites" in body


async def test_do_not_send_string_zero_allows_invite_field(test_candidate):
    """String ``"0"`` — the form our server produces for Python ``False`` — is
    accepted by the API. We do not assert an invite was actually sent (no
    real mailbox); the ``@example.invalid`` candidate email is undeliverable
    by design.
    """
    payload = {
        "title": _test_label("InviteStrZero"),
        "start_date": "2030-01-01T09:00:00Z",
        "end_date": "2030-01-01T10:00:00Z",
        "reminder": -1,
        "related_to": test_candidate,
        "related_to_type": "candidate",
        "attendee_candidates": test_candidate,
        "do_not_send_calendar_invites": "0",
    }
    created = await client.create_meeting(payload)
    meeting_id = created.get("id")
    assert meeting_id, f"Expected id in create-meeting response, got {created!r}"
    try:
        fetched = await client.get_meeting(meeting_id)
        assert fetched["id"] == meeting_id
    finally:
        await client.delete(f"/meetings/{meeting_id}")
