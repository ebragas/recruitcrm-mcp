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
                                 Default 1.0 (every tool call traced) so the
                                 Sentry MCP Dashboard populates with usage
                                 data out of the box. Set lower (e.g. 0.2)
                                 to reduce transaction volume on free plans.
"""

from __future__ import annotations

import logging
import os
import uuid
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


_DEFAULT_TRACES_RATE = 1.0


def _parse_traces_rate(raw: str | None) -> float:
    """Parse RECRUIT_CRM_MCP_SENTRY_TRACES_RATE, clamped to [0.0, 1.0].

    init_telemetry runs at module import; a malformed env var must not crash
    server startup. Falls back to the default rate with a warning.

    Default is 1.0 so the Sentry MCP Dashboard populates with per-tool usage
    data as soon as a DSN is configured — that's the whole point of pointing
    a DSN at this server. Users on tight quotas can dial it down via the
    env var.
    """
    if raw is None or raw == "":
        return _DEFAULT_TRACES_RATE
    try:
        value = float(raw)
    except ValueError:
        logger.warning(
            "RECRUIT_CRM_MCP_SENTRY_TRACES_RATE=%r is not a float; falling back to %s",
            raw,
            _DEFAULT_TRACES_RATE,
        )
        return _DEFAULT_TRACES_RATE
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
    # Stamp every span with a per-process ID. The MCP stdio transport has no
    # native session ID, and each tools/call is its own root trace, so without
    # this tag there's no way to group calls made within one server lifetime
    # (= one Claude Desktop launch). Lets dashboards answer "which tools get
    # called together in one session" and "what's the ordered sequence."
    sentry_sdk.set_tag("recruit_crm_mcp.process_id", uuid.uuid4().hex)
    logger.info("Sentry initialized for recruit-crm-mcp@%s", __version__)
    return True
