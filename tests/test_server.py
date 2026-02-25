from recruit_crm_mcp.server import ping


def test_ping_returns_ok():
    result = ping()
    assert result["status"] == "ok"
    assert result["version"] == "0.1.0"


def test_ping_reports_no_api_key(monkeypatch):
    monkeypatch.delenv("RECRUIT_CRM_API_KEY", raising=False)
    result = ping()
    assert result["api_configured"] is False


def test_ping_reports_api_key_configured(monkeypatch):
    monkeypatch.setenv("RECRUIT_CRM_API_KEY", "test-key")
    result = ping()
    assert result["api_configured"] is True
