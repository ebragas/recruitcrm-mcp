import pytest

from recruit_crm_mcp import client


@pytest.fixture(autouse=True)
async def reset_client():
    """Initialize the HTTP client before each test and close it after."""
    client.init_client()
    yield
    await client.aclose_client()
