"""Tests for the optional Sentry telemetry hook."""

import errno
import sys
from unittest.mock import patch

import pytest

from recruit_crm_mcp import telemetry
from recruit_crm_mcp.client import RecruitCrmError

try:
    from builtins import BaseExceptionGroup  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover - Python 3.10 fallback
    from exceptiongroup import BaseExceptionGroup  # type: ignore[no-redef]


def test_init_telemetry_no_op_without_dsn(monkeypatch):
    monkeypatch.delenv("RECRUIT_CRM_MCP_SENTRY_DSN", raising=False)
    monkeypatch.delenv("SENTRY_DSN", raising=False)
    with patch("sentry_sdk.init") as mock_init:
        assert telemetry.init_telemetry() is False
        mock_init.assert_not_called()


def test_init_telemetry_uses_recruit_specific_var(monkeypatch):
    monkeypatch.setenv(
        "RECRUIT_CRM_MCP_SENTRY_DSN", "https://abc@o1.ingest.sentry.io/123"
    )
    monkeypatch.delenv("SENTRY_DSN", raising=False)
    with patch("sentry_sdk.init") as mock_init:
        assert telemetry.init_telemetry() is True
        mock_init.assert_called_once()
        kwargs = mock_init.call_args.kwargs
        assert kwargs["dsn"] == "https://abc@o1.ingest.sentry.io/123"
        assert kwargs["send_default_pii"] is True
        assert kwargs["release"].startswith("recruit-crm-mcp@")


def test_init_telemetry_falls_back_to_sentry_dsn(monkeypatch):
    monkeypatch.delenv("RECRUIT_CRM_MCP_SENTRY_DSN", raising=False)
    monkeypatch.setenv("SENTRY_DSN", "https://fallback@o1.ingest.sentry.io/456")
    with patch("sentry_sdk.init") as mock_init:
        assert telemetry.init_telemetry() is True
        assert (
            mock_init.call_args.kwargs["dsn"]
            == "https://fallback@o1.ingest.sentry.io/456"
        )


def test_init_telemetry_recruit_var_takes_precedence(monkeypatch):
    monkeypatch.setenv(
        "RECRUIT_CRM_MCP_SENTRY_DSN", "https://primary@o1.ingest.sentry.io/123"
    )
    monkeypatch.setenv("SENTRY_DSN", "https://other@o1.ingest.sentry.io/999")
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert (
            mock_init.call_args.kwargs["dsn"]
            == "https://primary@o1.ingest.sentry.io/123"
        )


def test_init_telemetry_environment_default(monkeypatch):
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    monkeypatch.delenv("RECRUIT_CRM_MCP_ENV", raising=False)
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert mock_init.call_args.kwargs["environment"] == "production"


def test_init_telemetry_environment_override(monkeypatch):
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    monkeypatch.setenv("RECRUIT_CRM_MCP_ENV", "staging")
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert mock_init.call_args.kwargs["environment"] == "staging"


def test_init_telemetry_traces_rate(monkeypatch):
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_TRACES_RATE", "0.25")
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert mock_init.call_args.kwargs["traces_sample_rate"] == 0.25


def test_init_telemetry_traces_rate_default(monkeypatch):
    """Default is 1.0 so the Sentry MCP Dashboard populates with per-tool
    usage data the moment a DSN is configured. Pinned: lowering this is a
    user-visible behavior change that needs a CHANGELOG entry."""
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    monkeypatch.delenv("RECRUIT_CRM_MCP_SENTRY_TRACES_RATE", raising=False)
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert mock_init.call_args.kwargs["traces_sample_rate"] == 1.0


def test_init_telemetry_traces_rate_empty_string_uses_default(monkeypatch):
    """Empty string is treated identically to unset — both fall through to
    the default. Some shells export `FOO=` rather than unsetting."""
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_TRACES_RATE", "")
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert mock_init.call_args.kwargs["traces_sample_rate"] == 1.0


def test_init_telemetry_traces_rate_zero_disables_tracing(monkeypatch):
    """0.0 is a valid override — users on tight Sentry quotas can opt out
    of tracing entirely while still capturing errors."""
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_TRACES_RATE", "0.0")
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert mock_init.call_args.kwargs["traces_sample_rate"] == 0.0


def test_init_telemetry_traces_rate_invalid_falls_back(monkeypatch):
    """Bad traces-rate input must not crash module import (init_telemetry runs
    at import time in server.py). Falls back to the default rate."""
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_TRACES_RATE", "not-a-number")
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert mock_init.call_args.kwargs["traces_sample_rate"] == 1.0


def test_init_telemetry_traces_rate_clamped_above_one(monkeypatch):
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_TRACES_RATE", "5.0")
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert mock_init.call_args.kwargs["traces_sample_rate"] == 1.0


def test_init_telemetry_traces_rate_clamped_below_zero(monkeypatch):
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_TRACES_RATE", "-1.0")
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert mock_init.call_args.kwargs["traces_sample_rate"] == 0.0


def test_init_telemetry_registers_before_send(monkeypatch):
    """The before_send hook must be wired into sentry_sdk.init so that 4xx
    upstream errors can be filtered."""
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert mock_init.call_args.kwargs["before_send"] is telemetry._before_send


def _exc_info(exc: BaseException) -> tuple:
    """Build a sys.exc_info()-shaped tuple by raising and catching."""
    try:
        raise exc
    except BaseException:
        return sys.exc_info()


@pytest.mark.parametrize("status", [400, 404, 422, 429, 499])
def test_before_send_drops_4xx_upstream_errors(status):
    err = RecruitCrmError(status, {"message": "bad input"}, "GET", "/companies/1234")
    result = telemetry._before_send({"event": "x"}, {"exc_info": _exc_info(err)})
    assert result is None


@pytest.mark.parametrize("status", [500, 502, 503, 504])
def test_before_send_keeps_5xx_upstream_errors(status):
    err = RecruitCrmError(status, "boom", "POST", "/jobs")
    event = {"event": "x"}
    result = telemetry._before_send(event, {"exc_info": _exc_info(err)})
    assert result is event


def test_before_send_keeps_validation_error():
    """Pydantic / schema validation errors are server bugs (PYTHON-5/-7) we
    want to know about."""
    err = ValueError("schema validation failed")
    event = {"event": "x"}
    result = telemetry._before_send(event, {"exc_info": _exc_info(err)})
    assert result is event


def test_before_send_keeps_network_error():
    """httpx ConnectError / TimeoutException have no `status` attribute and
    must continue to capture."""
    import httpx

    err = httpx.ConnectError("DNS lookup failed")
    event = {"event": "x"}
    result = telemetry._before_send(event, {"exc_info": _exc_info(err)})
    assert result is event


def test_before_send_keeps_unhandled_exception():
    err = RuntimeError("unexpected")
    event = {"event": "x"}
    result = telemetry._before_send(event, {"exc_info": _exc_info(err)})
    assert result is event


def test_before_send_drops_4xx_wrapped_in_outer_exception():
    """FastMCP wraps tool exceptions; the RecruitCrmError sits behind
    __cause__. Filter must still drop the event."""
    inner = RecruitCrmError(404, "not found", "GET", "/companies/1234")
    try:
        try:
            raise inner
        except RecruitCrmError as e:
            raise RuntimeError("Tool failed") from e
    except RuntimeError:
        info = sys.exc_info()
    result = telemetry._before_send({"event": "x"}, {"exc_info": info})
    assert result is None


def test_before_send_no_exc_info_keeps_event():
    """Non-exception events (e.g. messages) pass through unchanged."""
    event = {"message": "hello"}
    result = telemetry._before_send(event, {})
    assert result is event


def test_before_send_drops_bare_broken_pipe():
    """Plain BrokenPipeError from stdio shutdown is benign noise."""
    err = BrokenPipeError(errno.EPIPE, "Broken pipe")
    result = telemetry._before_send({"event": "x"}, {"exc_info": _exc_info(err)})
    assert result is None


def test_before_send_drops_oserror_epipe():
    """Some shutdown paths surface EPIPE as OSError, not BrokenPipeError."""
    err = OSError(errno.EPIPE, "Broken pipe")
    result = telemetry._before_send({"event": "x"}, {"exc_info": _exc_info(err)})
    assert result is None


def test_before_send_drops_broken_pipe_inside_exception_group():
    """The real PYTHON-B stack: anyio's task group wraps EPIPE in a
    BaseExceptionGroup before it bubbles out of mcp.run()."""
    inner = BrokenPipeError(errno.EPIPE, "Broken pipe")
    group = BaseExceptionGroup("unhandled errors in a TaskGroup", [inner])
    result = telemetry._before_send({"event": "x"}, {"exc_info": _exc_info(group)})
    assert result is None


def test_before_send_drops_broken_pipe_via_cause_chain():
    """Same shape as the wrapped-4xx test — confirm chain-walking applies."""
    try:
        try:
            raise BrokenPipeError(errno.EPIPE, "Broken pipe")
        except BrokenPipeError as e:
            raise RuntimeError("transport closed") from e
    except RuntimeError:
        info = sys.exc_info()
    result = telemetry._before_send({"event": "x"}, {"exc_info": info})
    assert result is None


def test_before_send_keeps_exception_with_suppressed_broken_pipe_context():
    """``raise ... from None`` deliberately hides the prior context. The walker
    must respect ``__suppress_context__`` — otherwise a real bug whose handler
    happened to fire mid-EPIPE would be silently dropped."""
    try:
        try:
            raise BrokenPipeError(errno.EPIPE, "Broken pipe")
        except BrokenPipeError:
            raise RuntimeError("real bug surfaced during shutdown") from None
    except RuntimeError:
        info = sys.exc_info()
    event = {"event": "x"}
    result = telemetry._before_send(event, {"exc_info": info})
    assert result is event


def test_before_send_keeps_oserror_non_epipe():
    """Other OSError errnos (ENOSPC, EIO, …) are real bugs — must capture."""
    err = OSError(errno.ENOSPC, "No space left on device")
    event = {"event": "x"}
    result = telemetry._before_send(event, {"exc_info": _exc_info(err)})
    assert result is event


def test_before_send_keeps_unrelated_exception_group():
    """An ExceptionGroup that doesn't contain a BrokenPipeError must pass
    through — e.g. a TaskGroup surfacing real bugs."""
    group = BaseExceptionGroup("multi-failure", [RuntimeError("boom")])
    event = {"event": "x"}
    result = telemetry._before_send(event, {"exc_info": _exc_info(group)})
    assert result is event


def test_init_telemetry_stamps_process_id_tag(monkeypatch):
    """Every span emitted by one server lifetime should share a process_id
    tag so dashboards can group calls into "sessions" — stdio MCP has no
    native session ID, and each tools/call is its own root trace."""
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    with patch("sentry_sdk.init"), patch("sentry_sdk.set_tag") as mock_set_tag:
        telemetry.init_telemetry()
        keys = [call.args[0] for call in mock_set_tag.call_args_list]
        assert "recruit_crm_mcp.process_id" in keys
        process_id_value = next(
            call.args[1]
            for call in mock_set_tag.call_args_list
            if call.args[0] == "recruit_crm_mcp.process_id"
        )
        assert isinstance(process_id_value, str) and len(process_id_value) >= 16


def test_init_telemetry_process_id_unique_per_call(monkeypatch):
    """Each init call (= each server boot) gets a fresh process_id."""
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    with patch("sentry_sdk.init"), patch("sentry_sdk.set_tag") as mock_set_tag:
        telemetry.init_telemetry()
        telemetry.init_telemetry()
        ids = [
            call.args[1]
            for call in mock_set_tag.call_args_list
            if call.args[0] == "recruit_crm_mcp.process_id"
        ]
        assert len(ids) == 2
        assert ids[0] != ids[1]


def test_init_telemetry_suppresses_log_derived_events(monkeypatch):
    """FastMCP logs each tool exception, which would otherwise duplicate
    the MCPIntegration capture. Confirm LoggingIntegration is constructed
    with event_level=None so only the exception path produces events."""
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    with patch("sentry_sdk.init") as mock_init, patch(
        "sentry_sdk.integrations.logging.LoggingIntegration"
    ) as mock_logging_integration:
        telemetry.init_telemetry()

        mock_init.assert_called_once()
        mock_logging_integration.assert_called_once()
        assert mock_logging_integration.call_args.kwargs["event_level"] is None
