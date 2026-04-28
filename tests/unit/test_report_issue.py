"""Tests for the report_issue MCP tool."""

from urllib.parse import parse_qs, urlparse

import pytest

from recruit_crm_mcp.server import _REPORT_SUMMARY_MAX, report_issue


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
async def test_url_stays_under_limit_with_huge_summary():
    """A massive summary alone (no last_error) must not produce an unopenable URL.
    Earlier the fallback branch only triggered when last_error was set."""
    huge_summary = "Y" * 20_000
    result = await report_issue(huge_summary)
    assert len(result["url"]) <= 7000 + 200


@pytest.mark.anyio
async def test_url_stays_under_limit_with_huge_summary_and_extra():
    huge_summary = "Y" * 20_000
    huge_extra = "Z" * 5_000
    result = await report_issue(
        huge_summary, last_error="err", additional_context=huge_extra
    )
    assert len(result["url"]) <= 7000 + 200


@pytest.mark.anyio
async def test_no_truncation_note_when_no_last_error_provided():
    """When the user didn't supply a trace, the body must never claim one was
    dropped — even when other fields force the iterative shrink path."""
    huge_summary = "Y" * 20_000
    huge_extra = "Z" * 5_000
    result = await report_issue(
        huge_summary, last_error=None, additional_context=huge_extra
    )
    qs = parse_qs(urlparse(result["url"]).query)
    assert "Trace omitted" not in qs["body"][0]


@pytest.mark.anyio
async def test_no_truncation_note_when_last_error_blank():
    huge_summary = "Y" * 20_000
    result = await report_issue(huge_summary, last_error="", additional_context="")
    qs = parse_qs(urlparse(result["url"]).query)
    assert "Trace omitted" not in qs["body"][0]


@pytest.mark.anyio
async def test_truncation_note_appears_when_trace_was_dropped():
    """Force the candidate path that drops a provided trace by maxing every
    field. URL must still fit, and either the trace appears OR the note does."""
    result = await report_issue(
        summary="X" * _REPORT_SUMMARY_MAX,
        last_error="Y" * 2000,
        additional_context="Z" * 2000,
    )
    body = parse_qs(urlparse(result["url"]).query)["body"][0]
    assert len(result["url"]) <= 7000 + 200
    trace_chunk = "Y" * 100
    assert (trace_chunk in body) or ("Trace omitted" in body)
    # Mutually exclusive: never both
    assert not (trace_chunk in body and "Trace omitted" in body)


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
