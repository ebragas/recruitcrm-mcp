from recruit_crm_mcp.server import (
    ping,
    __version__,
    _summarize_candidate,
    _summarize_job,
    _summarize_user,
    _job_location_label,
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
        assert result["city"] is None


class TestSummarizeJob:
    def test_basic_fields(self):
        raw = {
            "slug": "17648707064020043135awk",
            "name": "Backend Engineer",
            "job_status": {"id": 1, "label": "Open"},
            "city": "Austin",
            "country": "US",
            "job_type": "Full-time",
            "job_location_type": "1",
            "minimum_experience": "2",
            "maximum_experience": "5",
            "min_annual_salary": "80000",
            "max_annual_salary": "120000",
            "pay_rate": "0",
            "bill_rate": "0",
            "job_category": "Engineering",
            "note_for_candidates": "Great team!",
            "job_description_file": None,
        }
        result = _summarize_job(raw)
        assert result["slug"] == "17648707064020043135awk"
        assert result["name"] == "Backend Engineer"
        assert result["status"] == "Open"
        assert result["city"] == "Austin"
        assert result["country"] == "US"
        assert result["job_type"] == "Full-time"
        assert result["job_location_type"] == "Remote"
        assert result["minimum_experience"] == "2"
        assert result["maximum_experience"] == "5"
        assert result["min_annual_salary"] == "80000"
        assert result["max_annual_salary"] == "120000"
        assert result["pay_rate"] == "0"
        assert result["bill_rate"] == "0"
        assert result["job_category"] == "Engineering"
        assert result["note_for_candidates"] == "Great team!"
        assert result["job_description_file"] is None

    def test_no_status(self):
        raw = {"slug": "abc", "name": "Designer"}
        result = _summarize_job(raw)
        assert result["slug"] == "abc"
        assert result["name"] == "Designer"
        assert result["status"] is None
        assert result["city"] is None
        assert result["country"] is None
        assert result["job_location_type"] == ""


class TestJobLocationLabel:
    def test_remote(self):
        assert _job_location_label("1") == "Remote"

    def test_hybrid(self):
        assert _job_location_label("2") == "Hybrid"

    def test_onsite(self):
        assert _job_location_label("0") == "On-site"

    def test_unknown_value(self):
        assert _job_location_label("99") == "99"

    def test_none(self):
        assert _job_location_label(None) == ""


class TestGetAssignedCandidatesSummarization:
    """Test that get_assigned_candidates produces correct summaries."""

    def test_summarizes_candidate_with_hiring_status(self):
        """Candidate fields + hiring_status from status label."""
        item = {
            "candidate": {
                "slug": "cand-123",
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane@example.com",
                "position": "Engineer",
                "current_organization": "Acme",
                "city": "Austin",
            },
            "status": {"id": 5, "label": "Interview"},
        }
        summary = _summarize_candidate(item["candidate"])
        status = item.get("status") or {}
        summary["hiring_status"] = status.get("label")

        assert summary["slug"] == "cand-123"
        assert summary["name"] == "Jane Doe"
        assert summary["email"] == "jane@example.com"
        assert summary["position"] == "Engineer"
        assert summary["company"] == "Acme"
        assert summary["city"] == "Austin"
        assert summary["hiring_status"] == "Interview"

    def test_missing_status_gives_none(self):
        """When status is missing, hiring_status should be None."""
        item = {
            "candidate": {"slug": "cand-456", "first_name": "John", "last_name": "Smith"},
        }
        summary = _summarize_candidate(item.get("candidate", {}))
        status = item.get("status") or {}
        summary["hiring_status"] = status.get("label")

        assert summary["slug"] == "cand-456"
        assert summary["hiring_status"] is None


class TestSummarizeUser:
    def test_basic_fields(self):
        raw = {
            "id": 43135,
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "role": "Admin",
        }
        result = _summarize_user(raw)
        assert result["id"] == 43135
        assert result["name"] == "Jane Doe"
        assert result["email"] == "jane@example.com"
        assert result["role"] == "Admin"

    def test_empty_record(self):
        result = _summarize_user({})
        assert result["id"] is None
        assert result["name"] == ""
        assert result["email"] is None
        assert result["role"] is None
