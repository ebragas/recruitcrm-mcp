import pytest

from recruit_crm_mcp import client


@pytest.fixture(autouse=True)
async def reset_client():
    """Reset the shared HTTP client between tests to avoid stale event loops."""
    yield
    await client.aclose_client()
