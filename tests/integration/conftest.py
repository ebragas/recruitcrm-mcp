import logging
import uuid

import pytest

from recruit_crm_mcp import client

logger = logging.getLogger(__name__)

TEST_ENTITY_PREFIX = "MCP-Test"


def _test_label() -> str:
    return f"{TEST_ENTITY_PREFIX}-{uuid.uuid4().hex[:8]}"


@pytest.fixture(autouse=True)
async def reset_client():
    """Initialize the HTTP client before each test and close it after."""
    client.init_client()
    yield
    await client.aclose_client()


@pytest.fixture
async def test_candidate():
    """Create a throwaway candidate for use as a write-test anchor.

    Orphans from crashed tests are identifiable by the ``MCP-Test-*`` prefix.
    """
    label = _test_label()
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
    label = _test_label()
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
    label = _test_label()
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
