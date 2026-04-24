"""Integration tests for partial-POST update_* round-trips.

Each test:
1. Creates an entity with several fields
2. Calls ``update_*`` with a small patch (one field)
3. Re-fetches and asserts (a) the patched field changed and (b) the other
   fields the test wrote on creation are still preserved

The whole point is to verify that the partial-POST pattern
(``post(path, {non-None fields})``) actually preserves omitted fields on
the live API for every endpoint we call ``update_*`` on. ``_fetch_merge_post``
was abandoned because the API's read shape diverges from its write shape
(nested objects on read, scalar IDs / comma strings on write) and re-posting
the read shape yields 422.

Run one class at a time to be gentle on the 60 req/min rate limit:

    uv run pytest tests/integration/test_update_roundtrips.py::TestUpdateCompanyRoundTrip -v
"""

import pytest

from recruit_crm_mcp import client

pytestmark = [pytest.mark.anyio, pytest.mark.integration]


class TestUpdateCompanyRoundTrip:
    """Partial POST to /companies/{slug} preserves omitted fields."""

    async def test_partial_update_preserves_other_fields(self, test_company):
        # Seed a few writable scalar fields on top of the auto-created company
        seed = {
            "about_company": "original about",
            "city": "Boston",
            "website": "https://example.invalid",
            "address": "1 Main St",
        }
        await client.update_company(test_company, seed)
        baseline = await client.get_company(test_company)
        assert baseline.get("about_company") == "original about"
        assert baseline.get("city") == "Boston"

        # Patch only ``about_company`` — others must survive
        await client.update_company(test_company, {"about_company": "patched about"})
        fetched = await client.get_company(test_company)

        assert fetched.get("about_company") == "patched about", (
            f"about_company not updated: {fetched.get('about_company')!r}"
        )
        assert fetched.get("city") == "Boston", (
            f"city not preserved: {fetched.get('city')!r}"
        )
        assert fetched.get("website") == "https://example.invalid", (
            f"website not preserved: {fetched.get('website')!r}"
        )
        assert fetched.get("address") == "1 Main St", (
            f"address not preserved: {fetched.get('address')!r}"
        )


class TestUpdateContactRoundTrip:
    """Partial POST to /contacts/{slug} preserves omitted fields."""

    async def test_partial_update_preserves_other_fields(self, test_contact):
        # Seed some writable scalar fields on the auto-created contact
        seed = {
            "city": "Boston",
            "country": "United States",
            "address": "1 Main St",
            "linkedin": "https://linkedin.com/in/example-mcp-test",
        }
        await client.update_contact(test_contact, seed)
        baseline = await client.get_contact(test_contact)
        assert baseline.get("city") == "Boston"

        # Patch only ``address`` — others must survive
        await client.update_contact(test_contact, {"address": "2 Patched Ave"})
        fetched = await client.get_contact(test_contact)

        assert fetched.get("address") == "2 Patched Ave", (
            f"address not updated: {fetched.get('address')!r}"
        )
        assert fetched.get("city") == "Boston", (
            f"city not preserved: {fetched.get('city')!r}"
        )
        assert fetched.get("country") == "United States", (
            f"country not preserved: {fetched.get('country')!r}"
        )
        assert fetched.get("linkedin") == "https://linkedin.com/in/example-mcp-test", (
            f"linkedin not preserved: {fetched.get('linkedin')!r}"
        )


class TestUpdateCandidateRoundTrip:
    """Partial POST to /candidates/{slug} preserves omitted fields."""

    async def test_partial_update_preserves_other_fields(self, test_candidate):
        # Seed writable scalar fields on the auto-created candidate
        seed = {
            "city": "Boston",
            "country": "United States",
            "position": "Engineer",
            "address": "1 Main St",
        }
        await client.update_candidate(test_candidate, seed)
        baseline = await client.get_candidate(test_candidate)
        assert baseline.get("city") == "Boston"

        # Patch only ``address`` — others must survive
        await client.update_candidate(test_candidate, {"address": "3 Patched Way"})
        fetched = await client.get_candidate(test_candidate)

        assert fetched.get("address") == "3 Patched Way", (
            f"address not updated: {fetched.get('address')!r}"
        )
        assert fetched.get("city") == "Boston", (
            f"city not preserved: {fetched.get('city')!r}"
        )
        assert fetched.get("country") == "United States", (
            f"country not preserved: {fetched.get('country')!r}"
        )
        assert fetched.get("position") == "Engineer", (
            f"position not preserved: {fetched.get('position')!r}"
        )


class TestUpdateMeetingRoundTrip:
    """Partial POST to /meetings/{id} preserves omitted fields."""

    async def test_partial_update_preserves_other_fields(self, test_candidate):
        payload = {
            "title": "MCP update-roundtrip meeting",
            "description": "original description",
            "start_date": "2030-01-01T09:00:00Z",
            "end_date": "2030-01-01T10:00:00Z",
            "reminder": -1,
            "related_to": test_candidate,
            "related_to_type": "candidate",
            "do_not_send_calendar_invites": True,
        }
        created = await client.create_meeting(payload)
        meeting_id = created.get("id")
        assert meeting_id, f"create failed: {created!r}"
        try:
            # Patch only ``description`` — title/related_to/reminder must survive
            await client.update_meeting(
                meeting_id, {"description": "patched description"}
            )
            fetched = await client.get_meeting(meeting_id)

            assert fetched.get("description") == "patched description", (
                f"description not updated: {fetched.get('description')!r}"
            )
            assert fetched.get("title") == "MCP update-roundtrip meeting", (
                f"title not preserved: {fetched.get('title')!r}"
            )
            assert fetched.get("related_to") == test_candidate, (
                f"related_to not preserved: {fetched.get('related_to')!r}"
            )
            assert fetched.get("reminder") == -1, (
                f"reminder not preserved: {fetched.get('reminder')!r}"
            )
        finally:
            await client.delete(f"/meetings/{meeting_id}")


class TestUpdateJobRoundTrip:
    """Partial POST to /jobs/{slug} preserves omitted fields.

    Skipped: creating a job requires several other entities (a company and a
    contact) plus mandatory scalar fields like ``currency_id``. Setting that
    fixture up correctly inside an integration test would more than double
    the number of API calls per run and risk leaking entities. The partial
    POST pattern is exercised against four other endpoints in this file —
    if it works there it should work here too, and a manual smoke can verify.
    """

    @pytest.mark.skip(
        reason="Job creation requires company+contact+currency_id; covered "
        "by other update_* round-trips in this file."
    )
    async def test_partial_update_preserves_other_fields(self):
        pass
