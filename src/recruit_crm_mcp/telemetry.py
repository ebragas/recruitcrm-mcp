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

import errno
import logging
import os
import uuid
from typing import Any

from recruit_crm_mcp import __version__
from recruit_crm_mcp.client import RecruitCrmError

try:
    from builtins import BaseExceptionGroup  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover - Python 3.10 fallback
    from exceptiongroup import BaseExceptionGroup  # type: ignore[no-redef]

logger = logging.getLogger(__name__)


def _is_self_benign(exc: BaseException) -> bool:
    """True if ``exc`` itself (ignoring its chain) is a known benign type:
    a 4xx upstream API error or an EPIPE from the stdio transport.
    """
    if isinstance(exc, BrokenPipeError):
        return True
    if isinstance(exc, OSError) and exc.errno == errno.EPIPE:
        return True
    if isinstance(exc, RecruitCrmError) and 400 <= exc.status < 500:
        return True
    return False


def _is_benign(
    exc: BaseException | None, _seen: set[int] | None = None
) -> bool:
    """True iff every actionable failure reachable from ``exc`` is benign noise.

    For a ``BaseExceptionGroup``, ALL child exceptions must be benign — anyio's
    task group can wrap one EPIPE alongside a real bug, and dropping the event
    in that case would silently swallow the real failure.

    For a non-group exception, the exception itself is the failure; ``__cause__``
    / ``__context__`` are historical context for the wrapping pattern
    (``raise OuterError() from underlying``). If the outer exception is a known
    benign type we drop; otherwise we follow the chain to the underlying cause.
    Respects ``__suppress_context__`` (set by ``raise ... from None``).
    """
    if exc is None:
        return False
    if _seen is None:
        _seen = set()
    if id(exc) in _seen:
        return False
    _seen.add(id(exc))

    if isinstance(exc, BaseExceptionGroup):
        return bool(exc.exceptions) and all(
            _is_benign(child, _seen) for child in exc.exceptions
        )

    if _is_self_benign(exc):
        return True
    if exc.__cause__ is not None:
        return _is_benign(exc.__cause__, _seen)
    if exc.__context__ is not None and not exc.__suppress_context__:
        return _is_benign(exc.__context__, _seen)
    return False


def _before_send(
    event: dict[str, Any], hint: dict[str, Any]
) -> dict[str, Any] | None:
    """Drop Sentry events that aren't real production bugs.

    Filters (see ``_is_self_benign`` for the exact match list):
    - 4xx responses from the upstream API: user-input errors (bad slugs,
      already-assigned candidates, etc.) the API surfaces correctly to
      the caller.
    - ``BrokenPipeError`` (and ``OSError`` with ``errno == EPIPE``, which some
      shutdown paths surface instead) from the stdio transport: benign
      client-disconnect noise on every shutdown, not a server bug.

    A mixed ``BaseExceptionGroup`` containing both a benign exception and a
    real failure is kept — see ``_is_benign``.

    5xx, network errors, ValidationError, and unhandled exceptions still
    capture normally.
    """
    exc_info = hint.get("exc_info")
    if exc_info and _is_benign(exc_info[1]):
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
