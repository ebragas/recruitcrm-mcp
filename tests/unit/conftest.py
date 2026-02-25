import pytest


@pytest.fixture(autouse=True)
def fake_api_key(monkeypatch):
    """Ensure unit tests never use a real API key."""
    monkeypatch.setenv("RECRUIT_CRM_API_KEY", "test-key-123")
