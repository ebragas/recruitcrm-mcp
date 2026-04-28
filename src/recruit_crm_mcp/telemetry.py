"""Optional Sentry error reporting.

Strictly opt-in via env var. No DSN is published or embedded — users who want
observability point the MCP at their own Sentry project. With no DSN set,
``init_telemetry()`` returns silently and nothing is sent over the network.

Env vars:
    RECRUIT_CRM_MCP_SENTRY_DSN   Project-specific DSN. Takes precedence.
    SENTRY_DSN                   Fallback DSN. Convenience for users who
                                 already have it set globally.
    RECRUIT_CRM_MCP_ENV          Sentry environment tag. Default: production.
    RECRUIT_CRM_MCP_SENTRY_TRACES_RATE
                                 Float 0.0-1.0 for tracing sample rate.
                                 Default 0.0 (tracing off).
"""

from __future__ import annotations

import logging
import os

from recruit_crm_mcp import __version__

logger = logging.getLogger(__name__)


def init_telemetry() -> bool:
    """Initialize Sentry if a DSN is configured. Returns True if initialized."""
    dsn = os.getenv("RECRUIT_CRM_MCP_SENTRY_DSN") or os.getenv("SENTRY_DSN")
    if not dsn:
        return False

    import sentry_sdk
    from sentry_sdk.integrations.logging import LoggingIntegration
    from sentry_sdk.integrations.mcp import MCPIntegration

    sentry_sdk.init(
        dsn=dsn,
        release=f"recruit-crm-mcp@{__version__}",
        environment=os.getenv("RECRUIT_CRM_MCP_ENV", "production"),
        # Users opt in by providing their own DSN; their Sentry project, their
        # data. Send full context so errors are actually triageable.
        send_default_pii=True,
        traces_sample_rate=float(
            os.getenv("RECRUIT_CRM_MCP_SENTRY_TRACES_RATE", "0.0")
        ),
        integrations=[
            MCPIntegration(include_prompts=True),
            # FastMCP logs every tool exception at error level before re-raising
            # as ToolError; Sentry's default LoggingIntegration would then file
            # a duplicate event for the same trace. Keep breadcrumbs, suppress
            # log-derived events — MCPIntegration captures the actual exception.
            LoggingIntegration(event_level=None),
        ],
    )
    logger.info("Sentry initialized for recruit-crm-mcp@%s", __version__)
    return True
