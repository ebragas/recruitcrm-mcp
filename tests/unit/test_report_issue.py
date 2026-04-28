"""Tests for the report_issue MCP tool."""

from urllib.parse import parse_qs, urlparse

import pytest

from recruit_crm_mcp.server import report_issue


@pytest.mark.anyio
async def test_returns_prefilled_github_url():
    result = await report_issue("Tools fail on Vandelay job")
    parsed = urlparse(result["url"])
    assert parsed.scheme == "https"
    assert parsed.netloc == "github.com"
    assert parsed.path == "/ebragas/recruitcrm-mcp/issues/new"
    qs = parse_qs(parsed.query)
    assert qs["title"] == ["Tools fail on Vandelay job"]
    assert qs["labels"] == ["user-report"]
    assert "## Summary" in qs["body"][0]
    assert "Tools fail on Vandelay job" in qs["body"][0]
    assert "## Environment" in qs["body"][0]
    assert "recruit-crm-mcp:" in qs["body"][0]


@pytest.mark.anyio
async def test_includes_last_error_in_body():
    err = "ValidationError: 6 validation errors for JobSummary\nminimum_experience\n  Input should be a valid string"
    result = await report_issue("List jobs broken", last_error=err)
    qs = parse_qs(urlparse(result["url"]).query)
    assert "## Last error" in qs["body"][0]
    assert "ValidationError" in qs["body"][0]


@pytest.mark.anyio
async def test_includes_additional_context():
    result = await report_issue(
        "List jobs broken",
        additional_context="User was on Windows, ran via Claude Desktop",
    )
    qs = parse_qs(urlparse(result["url"]).query)
    assert "## Additional context" in qs["body"][0]
    assert "Windows" in qs["body"][0]


@pytest.mark.anyio
async def test_truncates_oversized_last_error():
    huge_error = "X" * 10_000
    result = await report_issue("Big error", last_error=huge_error)
    assert len(result["url"]) <= 7000 + 200  # tolerance for env block
    qs = parse_qs(urlparse(result["url"]).query)
    body = qs["body"][0]
    # When the trace is truncated due to URL length, it's dropped entirely with
    # a placeholder rather than partially included.
    assert "Trace omitted" in body or len(body) < len(huge_error)


@pytest.mark.anyio
async def test_title_falls_back_when_summary_blank():
    result = await report_issue("")
    qs = parse_qs(urlparse(result["url"]).query)
    assert qs["title"] == ["Bug report"]


@pytest.mark.anyio
async def test_title_uses_first_line_of_summary():
    result = await report_issue("First line summary\nSecond line detail\nThird")
    qs = parse_qs(urlparse(result["url"]).query)
    assert qs["title"] == ["First line summary"]


@pytest.mark.anyio
async def test_returns_instruction_to_user():
    result = await report_issue("anything")
    assert "url" in result
    assert "title" in result
    assert "instruction" in result
    assert "browser" in result["instruction"].lower()
