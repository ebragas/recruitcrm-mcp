"""Tests for the optional Sentry telemetry hook."""

from unittest.mock import patch

from recruit_crm_mcp import telemetry


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
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    monkeypatch.delenv("RECRUIT_CRM_MCP_SENTRY_TRACES_RATE", raising=False)
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert mock_init.call_args.kwargs["traces_sample_rate"] == 0.0


def test_init_telemetry_traces_rate_invalid_falls_back(monkeypatch):
    """Bad traces-rate input must not crash module import (init_telemetry runs
    at import time in server.py)."""
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_DSN", "https://x@o1.ingest.sentry.io/1")
    monkeypatch.setenv("RECRUIT_CRM_MCP_SENTRY_TRACES_RATE", "not-a-number")
    with patch("sentry_sdk.init") as mock_init:
        telemetry.init_telemetry()
        assert mock_init.call_args.kwargs["traces_sample_rate"] == 0.0


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
