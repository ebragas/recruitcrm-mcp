#!/usr/bin/env python
"""Smoke test: spawn the packaged MCP server via ``uvx`` and invoke tools end-to-end.

Verifies the entrypoint, stdio framing, and tool dispatch work as a cohesive
system — catches integration bugs that unit/MCP-layer tests can't see because
they skip the packaging + subprocess boundary.

Usage:
    uv run scripts/smoke.py                    # install from local working tree
    uv run scripts/smoke.py --from-pypi         # install from published PyPI wheel
    RCRM_SMOKE_WRITES=1 uv run scripts/smoke.py # also exercise a write round-trip

Exits 0 on success, non-zero on any failure.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import UvxStdioTransport


async def run_smoke(from_pypi: bool, exercise_writes: bool) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    transport = UvxStdioTransport(
        tool_name="recruit-crm-mcp",
        from_package=None if from_pypi else str(repo_root),
        env_vars={"RECRUIT_CRM_API_KEY": os.environ["RECRUIT_CRM_API_KEY"]},
    )

    async with Client(transport) as c:
        print("[smoke] connected via uvx stdio")

        tools = await c.list_tools()
        print(f"[smoke] list_tools returned {len(tools)} tools")
        assert len(tools) >= 30, f"expected >=30 tools, got {len(tools)}"

        ping = await c.call_tool("ping", {})
        assert ping.structured_content.get("status") == "ok", f"ping failed: {ping!r}"
        print(f"[smoke] ping ok (version={ping.structured_content.get('version')})")

        note_types = await c.call_tool("list_note_types", {})
        print(f"[smoke] list_note_types returned {len(note_types.structured_content.get('result', []))} types")

        if exercise_writes:
            print("[smoke] exercising write round-trip (candidate → note → delete both)")
            cand = await c.call_tool("create_candidate", {
                "first_name": "Smoke",
                "last_name": "Test",
                "email": "smoke-test@example.invalid",
            })
            cand_slug = cand.structured_content["id"]
            try:
                note = await c.call_tool("create_note", {
                    "description": "smoke test note",
                    "related_to": {"kind": "candidate", "id": cand_slug},
                })
                note_id = note.structured_content["id"]
                print(f"[smoke] created note {note_id} on candidate {cand_slug}")
                await c.call_tool("delete_note", {"note_id": int(note_id)})
                print(f"[smoke] deleted note {note_id}")
            finally:
                # Cleanup — best-effort, no delete_candidate MCP tool so use raw path
                import httpx

                async with httpx.AsyncClient() as http:
                    resp = await http.delete(
                        f"https://api.recruitcrm.io/v1/candidates/{cand_slug}",
                        headers={"Authorization": f"Bearer {os.environ['RECRUIT_CRM_API_KEY']}"},
                    )
                    if resp.is_success:
                        print(f"[smoke] deleted candidate {cand_slug}")
                    else:
                        print(
                            f"[smoke] WARNING: orphan candidate {cand_slug} "
                            f"(DELETE returned {resp.status_code})",
                            file=sys.stderr,
                        )

    print("[smoke] PASSED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from-pypi",
        action="store_true",
        help="Install from published PyPI wheel (default: local working tree)",
    )
    args = parser.parse_args()
    exercise_writes = os.environ.get("RCRM_SMOKE_WRITES") == "1"

    if "RECRUIT_CRM_API_KEY" not in os.environ:
        print("[smoke] ERROR: RECRUIT_CRM_API_KEY must be set", file=sys.stderr)
        return 2

    return asyncio.run(run_smoke(from_pypi=args.from_pypi, exercise_writes=exercise_writes))


if __name__ == "__main__":
    sys.exit(main())
