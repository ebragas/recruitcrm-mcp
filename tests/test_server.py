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
            "id": "abc123",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "job_title": "Engineer",
            "company_name": "Acme",
            "city": "Austin",
        }
        result = _summarize_candidate(raw)
        assert result["id"] == "abc123"
        assert result["name"] == "Jane Doe"
        assert result["email"] == "jane@example.com"
        assert result["job_title"] == "Engineer"
        assert result["company"] == "Acme"
        assert result["city"] == "Austin"

    def test_fallback_fields(self):
        raw = {
            "slug": "jane-doe",
            "first_name": "Jane",
            "last_name": "",
            "position": "Manager",
            "company": "BigCo",
        }
        result = _summarize_candidate(raw)
        assert result["id"] == "jane-doe"
        assert result["name"] == "Jane"
        assert result["job_title"] == "Manager"
        assert result["company"] == "BigCo"

    def test_empty_record(self):
        result = _summarize_candidate({})
        assert result["id"] is None
        assert result["name"] == ""
        assert result["email"] is None


class TestSummarizeJob:
    def test_basic_fields(self):
        raw = {
            "id": "job-1",
            "name": "Backend Engineer",
            "status": "Open",
            "city": "Austin",
            "country": "US",
        }
        result = _summarize_job(raw)
        assert result["id"] == "job-1"
        assert result["name"] == "Backend Engineer"
        assert result["status"] == "Open"
        assert result["city"] == "Austin"
        assert result["country"] == "US"

    def test_fallback_fields(self):
        raw = {"slug": "be-1", "title": "Frontend Dev"}
        result = _summarize_job(raw)
        assert result["id"] == "be-1"
        assert result["name"] == "Frontend Dev"
