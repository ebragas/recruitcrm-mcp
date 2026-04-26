import logging
import os
import uuid

import pytest

from recruit_crm_mcp import client

from tests.integration._sweep import sweep_orphans

logger = logging.getLogger(__name__)

TEST_ENTITY_PREFIX = "MCP-Test"


def _test_label(descriptor: str) -> str:
    """Return a canonical test entity label: ``MCP-Test-<descriptor>-<uuid8>``.

    Every integration test entity name MUST start with ``MCP-Test-`` so the
    session-end sweep can identify and delete orphans without risk to real
    tenant data. The descriptor is purely human-readable when scanning the
    live tenant.
    """
    return f"{TEST_ENTITY_PREFIX}-{descriptor}-{uuid.uuid4().hex[:8]}"


@pytest.fixture(autouse=True)
async def reset_client():
    """Initialize the HTTP client before each test and close it after."""
    client.init_client()
    yield
    await client.aclose_client()


@pytest.fixture(autouse=True)
def _maybe_keep_entities(monkeypatch):
    """When ``RECRUIT_CRM_KEEP_ENTITIES=1`` is set, no-op every ``client.delete``
    and ``client.delete_note`` call so test entities persist in the tenant
    for UI verification. Implies ``RECRUIT_CRM_SKIP_SWEEP=1`` (otherwise the
    session sweep would delete the entities you wanted to inspect).

    Run ``make integration-sweep`` afterwards to clean up.

    Stepping workflow:
        # 1. List node IDs
        uv run pytest -m integration --collect-only -q
        # 2. Run one test, leave entities for inspection
        RECRUIT_CRM_KEEP_ENTITIES=1 uv run pytest <node_id> -v -s
        # 3. Verify in the Recruit CRM UI
        # 4. Clean up
        make integration-sweep
    """
    if not os.environ.get("RECRUIT_CRM_KEEP_ENTITIES"):
        return
    os.environ.setdefault("RECRUIT_CRM_SKIP_SWEEP", "1")

    async def _noop_delete(path, params=None):
        print(f"[keep] would DELETE {path} — skipped")
        return None

    async def _noop_delete_note(note_id):
        print(f"[keep] would DELETE /notes/{note_id} — skipped")
        return None

    monkeypatch.setattr(client, "delete", _noop_delete)
    monkeypatch.setattr(client, "delete_note", _noop_delete_note)


@pytest.fixture(scope="session", autouse=True)
async def _orphan_sweep_session():
    """Session-end orphan sweep — backstop cleanup for any test whose own
    ``finally`` block didn't run (process kill, transient delete error,
    assertion mid-cleanup chain). Runs after the last integration test.

    Set ``RECRUIT_CRM_SKIP_SWEEP=1`` to disable for ad-hoc debugging where
    you want to inspect leftovers manually.
    """
    yield
    if os.environ.get("RECRUIT_CRM_SKIP_SWEEP"):
        logger.info("Orphan sweep skipped (RECRUIT_CRM_SKIP_SWEEP set)")
        return
    client.init_client()
    try:
        counts = await sweep_orphans()
        logger.info("Orphan sweep summary: %s", counts)
        print(f"\n[integration sweep] {counts}")
    finally:
        await client.aclose_client()


@pytest.fixture
async def test_candidate():
    """Create a throwaway candidate for use as a write-test anchor.

    Orphans from crashed tests are identifiable by the ``MCP-Test-*`` prefix.
    """
    label = _test_label("Cand")
    slug = None
    try:
        resp = await client.post("/candidates", {
            "first_name": label,
            "last_name": "Fixture",
            "email": f"{label.lower()}@example.invalid",
        })
        slug = resp.get("slug") if isinstance(resp, dict) else None
        if not slug:
            pytest.skip(f"Could not create test candidate: {resp!r}")
        yield slug
    finally:
        if slug:
            try:
                await client.delete(f"/candidates/{slug}")
            except Exception as exc:
                logger.warning("Orphaned test candidate %s: %s", slug, exc)


@pytest.fixture
async def test_contact():
    """Create a throwaway contact for use as a write-test anchor."""
    label = _test_label("Contact")
    slug = None
    try:
        resp = await client.post("/contacts", {
            "first_name": label,
            "last_name": "Fixture",
            "email": f"{label.lower()}@example.invalid",
        })
        slug = resp.get("slug") if isinstance(resp, dict) else None
        if not slug:
            pytest.skip(f"Could not create test contact: {resp!r}")
        yield slug
    finally:
        if slug:
            try:
                await client.delete(f"/contacts/{slug}")
            except Exception as exc:
                logger.warning("Orphaned test contact %s: %s", slug, exc)


@pytest.fixture
async def test_company():
    """Create a throwaway company for use as a write-test anchor."""
    label = _test_label("Co")
    slug = None
    try:
        resp = await client.post("/companies", {"company_name": label})
        slug = resp.get("slug") if isinstance(resp, dict) else None
        if not slug:
            pytest.skip(f"Could not create test company: {resp!r}")
        yield slug
    finally:
        if slug:
            try:
                await client.delete(f"/companies/{slug}")
            except Exception as exc:
                logger.warning("Orphaned test company %s: %s", slug, exc)
