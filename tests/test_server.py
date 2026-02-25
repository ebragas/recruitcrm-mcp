from recruit_crm_mcp.server import (
    ping,
    __version__,
    _summarize_candidate,
    _summarize_job,
)


def test_ping_returns_ok():
    result = ping()
    assert result["status"] == "ok"
    assert result["version"] == __version__


def test_ping_reports_no_api_key(monkeypatch):
    monkeypatch.delenv("RECRUIT_CRM_API_KEY", raising=False)
    result = ping()
    assert result["api_configured"] is False


def test_ping_reports_api_key_configured(monkeypatch):
    monkeypatch.setenv("RECRUIT_CRM_API_KEY", "test-key")
    result = ping()
    assert result["api_configured"] is True


class TestSummarizeCandidate:
    def test_basic_fields(self):
        raw = {
            "slug": "17720468790770031585gzy",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "position": "Engineer",
            "current_organization": "Acme",
            "city": "Austin",
        }
        result = _summarize_candidate(raw)
        assert result["slug"] == "17720468790770031585gzy"
        assert result["name"] == "Jane Doe"
        assert result["email"] == "jane@example.com"
        assert result["position"] == "Engineer"
        assert result["company"] == "Acme"
        assert result["city"] == "Austin"

    def test_empty_record(self):
        result = _summarize_candidate({})
        assert result["slug"] is None
        assert result["name"] == ""
        assert result["email"] is None
        assert result["position"] is None
        assert result["company"] is None


class TestSummarizeJob:
    def test_basic_fields(self):
        raw = {
            "slug": "17648707064020043135awk",
            "name": "Backend Engineer",
            "job_status": {"id": 1, "label": "Open"},
            "city": "Austin",
            "country": "US",
        }
        result = _summarize_job(raw)
        assert result["slug"] == "17648707064020043135awk"
        assert result["name"] == "Backend Engineer"
        assert result["status"] == "Open"
        assert result["city"] == "Austin"
        assert result["country"] == "US"

    def test_no_status(self):
        raw = {"slug": "abc", "name": "Designer"}
        result = _summarize_job(raw)
        assert result["slug"] == "abc"
        assert result["name"] == "Designer"
        assert result["status"] is None
