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
from typing import Any

from recruit_crm_mcp import __version__
from recruit_crm_mcp.client import RecruitCrmError

logger = logging.getLogger(__name__)


def _is_upstream_4xx(exc: BaseException | None) -> bool:
    """Walk the exception chain looking for a 4xx upstream API error.

    FastMCP wraps tool exceptions, so the original RecruitCrmError may sit
    behind __cause__ / __context__ links. Any 4xx anywhere in the chain
    means the event is rooted in a user-side error from the upstream API.
    """
    seen: set[int] = set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        if isinstance(exc, RecruitCrmError) and 400 <= exc.status < 500:
            return True
        exc = exc.__cause__ or exc.__context__
    return False


def _before_send(
    event: dict[str, Any], hint: dict[str, Any]
) -> dict[str, Any] | None:
    """Drop Sentry events caused by 4xx responses from the upstream API.

    These are user-input errors (bad slugs, already-assigned candidates, etc.)
    that the API surfaces correctly to the caller — they aren't production
    bugs. 5xx, network errors, ValidationError, and unhandled exceptions
    still capture normally.
    """
    exc_info = hint.get("exc_info")
    if exc_info and _is_upstream_4xx(exc_info[1]):
        return None
    return event


def _parse_traces_rate(raw: str | None) -> float:
    """Parse RECRUIT_CRM_MCP_SENTRY_TRACES_RATE, clamped to [0.0, 1.0].

    init_telemetry runs at module import; a malformed env var must not crash
    server startup. Falls back to 0.0 (tracing off) with a warning.
    """
    if raw is None or raw == "":
        return 0.0
    try:
        value = float(raw)
    except ValueError:
        logger.warning(
            "RECRUIT_CRM_MCP_SENTRY_TRACES_RATE=%r is not a float; falling back to 0.0",
            raw,
        )
        return 0.0
    return max(0.0, min(1.0, value))


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
        traces_sample_rate=_parse_traces_rate(
            os.getenv("RECRUIT_CRM_MCP_SENTRY_TRACES_RATE")
        ),
        before_send=_before_send,
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
