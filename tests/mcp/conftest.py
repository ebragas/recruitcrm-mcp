"""Shared fixtures for MCP dispatch-layer tests.

These tests exercise the FastMCP in-process dispatch (``fastmcp.Client(mcp)``)
rather than calling ``recruit_crm_mcp.client`` helpers directly. That way bugs
in the tool wrappers in ``server.py`` (payload assembly, ``EntityRef.kind``
mapping, ``_build_payload`` shape, etc.) are caught by CI.
"""

import logging
import uuid

import pytest
from fastmcp import Client

from recruit_crm_mcp import client
from recruit_crm_mcp.server import mcp

logger = logging.getLogger(__name__)

# Every module under tests/mcp/ is async + tagged with the `mcp` marker so we
# can run them in isolation via ``pytest -m mcp``.
pytestmark = [pytest.mark.anyio, pytest.mark.mcp]


TEST_ENTITY_PREFIX = "MCP-Test"


def _test_label() -> str:
    return f"{TEST_ENTITY_PREFIX}-{uuid.uuid4().hex[:8]}"


@pytest.fixture
async def mcp_client():
    """Open an in-process FastMCP ``Client`` bound to the real ``mcp`` server.

    The ``_lifespan`` handler in ``server.py`` (which calls
    ``client.init_client()``) runs automatically on connect and teardown.
    """
    async with Client(mcp) as c:
        yield c


# ---------------------------------------------------------------------------
# Live-backend fixtures — copied verbatim from tests/integration/conftest.py.
# Only needed by tests marked ``mcp_live``; safe to leave unused otherwise.
# ---------------------------------------------------------------------------


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
