"""Integration tests covering gaps in the TestWrites suite.

The primary TestWrites class in test_api.py only exercises
``related_to_type="candidate"``. This module adds:

1. Per-anchor round-trip coverage for ``related_to_type`` values
   (contact, company, job) on the create-note endpoint.
2. A rejection guard locking in the API's 4xx response to
   ``related_to_type="banana"`` so future API changes are caught.
3. Attendee comma-string contract verification for the create-meeting
   endpoint.

Every test cleans up its throwaway records in a try/finally. Job-anchor
coverage builds a full company/contact/job chain inline since no
``test_job`` fixture exists.
"""

import uuid

import pytest

from recruit_crm_mcp import client
from recruit_crm_mcp.client import RecruitCrmError

pytestmark = [pytest.mark.anyio, pytest.mark.integration]


async def test_create_note_for_contact(test_contact):
    """Anchor a note to a contact — verifies ``related_to_type='contact'``."""
    created = await client.create_note({
        "description": "MCP variant test (contact anchor)",
        "related_to": test_contact,
        "related_to_type": "contact",
    })
    note_id = created.get("id")
    assert note_id, f"Expected id in create-note response, got {created!r}"
    try:
        fetched = await client.get_note(note_id)
        assert fetched["id"] == note_id
        assert fetched.get("related_to") == test_contact
        assert fetched.get("related_to_type") == "contact"
    finally:
        await client.delete(f"/notes/{note_id}")


async def test_create_note_for_company(test_company):
    """Anchor a note to a company — verifies ``related_to_type='company'``."""
    created = await client.create_note({
        "description": "MCP variant test (company anchor)",
        "related_to": test_company,
        "related_to_type": "company",
    })
    note_id = created.get("id")
    assert note_id, f"Expected id in create-note response, got {created!r}"
    try:
        fetched = await client.get_note(note_id)
        assert fetched["id"] == note_id
        assert fetched.get("related_to") == test_company
        assert fetched.get("related_to_type") == "company"
    finally:
        await client.delete(f"/notes/{note_id}")


async def test_create_note_for_job():
    """Anchor a note to a job — verifies ``related_to_type='job'``.

    Builds a full company/contact/job chain inline since no ``test_job``
    fixture exists (job creation requires 6+ fields including
    ``currency_id`` and ``contact_slug``). All entities are torn down in
    reverse creation order (note -> job -> contact -> company).
    """
    label = f"MCP-Test-{uuid.uuid4().hex[:8]}"

    company_slug = None
    contact_slug = None
    job_slug = None
    note_id = None
    try:
        # (a) company to satisfy company_slug on the job
        company_resp = await client.post("/companies", {"company_name": label})
        company_slug = (
            company_resp.get("slug") if isinstance(company_resp, dict) else None
        )
        if not company_slug:
            pytest.skip(f"Could not create test company: {company_resp!r}")

        # (b) contact to satisfy contact_slug on the job.
        # The job API requires the contact to be already linked to the company
        # (422 otherwise), so we pass company_slug on the contact create.
        contact_resp = await client.post("/contacts", {
            "first_name": label,
            "last_name": "JobOwner",
            "email": f"{label.lower()}-owner@example.invalid",
            "company_slug": company_slug,
        })
        contact_slug = (
            contact_resp.get("slug") if isinstance(contact_resp, dict) else None
        )
        if not contact_slug:
            pytest.skip(f"Could not create test contact: {contact_resp!r}")

        # (c) job itself
        try:
            job_resp = await client.post("/jobs", {
                "name": label,
                "number_of_openings": 1,
                "company_slug": company_slug,
                "contact_slug": contact_slug,
                "currency_id": 1,
                "job_description_text": "test",
                "enable_job_application_form": 1,
            })
        except RecruitCrmError as exc:
            pytest.skip(
                f"Could not create test job (status {exc.status}): {exc.body!r}"
            )

        job_slug = job_resp.get("slug") if isinstance(job_resp, dict) else None
        if not job_slug:
            pytest.skip(f"Could not create test job: {job_resp!r}")

        created = await client.create_note({
            "description": "MCP variant test (job anchor)",
            "related_to": job_slug,
            "related_to_type": "job",
        })
        note_id = created.get("id")
        assert note_id, f"Expected id in create-note response, got {created!r}"

        fetched = await client.get_note(note_id)
        assert fetched["id"] == note_id
        assert fetched.get("related_to") == job_slug
        assert fetched.get("related_to_type") == "job"
    finally:
        # Tear down in reverse order so parent-child references don't block.
        if note_id is not None:
            try:
                await client.delete(f"/notes/{note_id}")
            except Exception:
                pass
        if job_slug is not None:
            try:
                await client.delete(f"/jobs/{job_slug}")
            except Exception:
                pass
        if contact_slug is not None:
            try:
                await client.delete(f"/contacts/{contact_slug}")
            except Exception:
                pass
        if company_slug is not None:
            try:
                await client.delete(f"/companies/{company_slug}")
            except Exception:
                pass


async def test_create_note_rejects_invalid_related_to_type(test_candidate):
    """Rejection guard: the API must reject bogus ``related_to_type`` values.

    Per CLAUDE.md's TDD rule, we lock in known API rejections as integration
    tests so future API behavior changes are caught.
    """
    with pytest.raises(RecruitCrmError) as exc_info:
        await client.create_note({
            "description": "reject me",
            "related_to": test_candidate,
            "related_to_type": "banana",
        })

    err = exc_info.value
    assert 400 <= err.status < 500, (
        f"Expected 4xx rejection for bogus related_to_type, got {err.status}"
    )
    assert err.body is not None, "Expected an error body describing the rejection"


async def test_log_meeting_attendee_candidate_round_trips(test_candidate):
    """Verify the ``_join`` attendee contract round-trips.

    Passing a comma-separated string of candidate slugs (here, just one)
    as ``attendee_candidates`` should result in the candidate being attached
    to the meeting.

    Note on response shape: the live API does NOT echo ``attendee_candidates``
    back on GET (it's ``None``). Instead, it exposes a separate ``attendees``
    list of dicts with ``attendee_id``/``attendee_type``/``display_name`` keys.
    ``attendee_id`` is the candidate slug. Example:
        {
          "attendee_id": "<candidate_slug>",
          "attendee_type": "Candidate",
          "display_name": "First Last",
        }
    """
    created = await client.create_meeting({
        "title": "MCP attendee round-trip",
        "start_date": "2030-01-01T09:00:00Z",
        "end_date": "2030-01-01T10:00:00Z",
        "reminder": -1,
        "related_to": test_candidate,
        "related_to_type": "candidate",
        "attendee_candidates": test_candidate,  # comma-string of 1
        "do_not_send_calendar_invites": "1",
    })
    meeting_id = created.get("id")
    assert meeting_id, f"Expected id in create-meeting response, got {created!r}"
    try:
        fetched = await client.get_meeting(meeting_id)
        attendees = fetched.get("attendees") or []
        assert isinstance(attendees, list), (
            f"Expected 'attendees' to be a list, got {type(attendees).__name__}: "
            f"{attendees!r}"
        )
        attendee_ids = [
            a.get("attendee_id") for a in attendees if isinstance(a, dict)
        ]
        assert test_candidate in attendee_ids, (
            f"Expected candidate slug {test_candidate!r} in attendees, "
            f"got {attendees!r}"
        )
        # Verify the attendee_type tag, since _join is specifically routing
        # the slug into the candidate bucket (not contact/user).
        candidate_attendee = next(
            (a for a in attendees if a.get("attendee_id") == test_candidate),
            None,
        )
        assert candidate_attendee is not None
        assert candidate_attendee.get("attendee_type") == "Candidate", (
            f"Expected attendee_type='Candidate', got "
            f"{candidate_attendee.get('attendee_type')!r}"
        )
    finally:
        await client.delete(f"/meetings/{meeting_id}")
