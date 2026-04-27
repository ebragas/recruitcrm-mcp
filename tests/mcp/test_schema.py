"""Schema + dispatch-layer smoke tests for the FastMCP server.

These tests do NOT hit the live Recruit CRM API. They verify:

* The in-process ``fastmcp.Client(mcp)`` transport dispatches tools correctly
  (``ping`` is safe because it only reads env — no HTTP).
* ``list_tools()`` returns every registered tool with a populated description.
* Write-tool input schemas expose the expected required fields so agents get
  useful validation errors rather than silent payload drops.
* ``EntityRef.kind`` is surfaced as an enum in the JSON schema (so MCP clients
  can present it as a dropdown, not a free-text field).
"""

from __future__ import annotations

import pytest

pytestmark = [pytest.mark.anyio, pytest.mark.mcp]

EXPECTED_RELATED_KINDS = {"candidate", "contact", "company", "job", "deal"}


def _input_schema(tool) -> dict:
    """Return the tool's JSON Schema as a dict regardless of attr/dict shape."""
    schema = getattr(tool, "inputSchema", None)
    if schema is None and isinstance(tool, dict):
        schema = tool.get("inputSchema")
    assert isinstance(schema, dict), f"inputSchema missing or wrong type on {tool!r}"
    return schema


def _find_kind_enum(schema: dict) -> list[str] | None:
    """Walk a JSON schema looking for the ``kind`` property of an EntityRef.

    FastMCP may inline nested Pydantic models directly under a parent
    property (``properties.related_to.properties.kind``) or via ``$defs``
    depending on version. Walk both shapes.
    """

    def _kind_from_properties(props: dict) -> list[str] | None:
        kind = props.get("kind")
        if isinstance(kind, dict) and isinstance(kind.get("enum"), list):
            return list(kind["enum"])
        return None

    def _walk(node: dict) -> list[str] | None:
        if not isinstance(node, dict):
            return None
        props = node.get("properties") or {}
        enum = _kind_from_properties(props)
        if enum:
            return enum
        # Recurse into any nested property schemas (e.g. related_to object)
        for child in props.values():
            found = _walk(child) if isinstance(child, dict) else None
            if found:
                return found
        # $defs — alternate shape where EntityRef is referenced
        for defn in (node.get("$defs") or {}).values():
            found = _walk(defn) if isinstance(defn, dict) else None
            if found:
                return found
        return None

    return _walk(schema)


async def test_ping_via_mcp_layer(mcp_client):
    """``ping`` dispatched through FastMCP returns the expected status dict."""
    result = await mcp_client.call_tool("ping", {})

    # FastMCP parses structured output back into the declared return type;
    # ``data`` should be the dict ``ping`` returned.
    data = result.data
    assert isinstance(data, dict), f"expected dict payload, got {type(data).__name__}"
    assert data.get("status") == "ok"
    assert "version" in data
    assert "api_configured" in data
    assert isinstance(data["api_configured"], bool)


async def test_list_tools_returns_expected_count(mcp_client):
    """Guard against accidental tool de-registration.

    We have 33+ tool registrations in ``server.py``; the absolute count is
    not as interesting as the floor — if this drops sharply, someone removed
    tools without updating tests.
    """
    tools = await mcp_client.list_tools()
    assert len(tools) >= 30, f"only {len(tools)} tools registered; expected >= 30"


async def test_every_tool_has_description(mcp_client):
    """Agent UX depends on descriptions — none may be empty."""
    tools = await mcp_client.list_tools()
    missing = [t.name for t in tools if not (t.description or "").strip()]
    assert not missing, f"tools missing description: {missing}"


async def test_write_tool_schemas_have_required_params(mcp_client):
    """``create_note``/``log_meeting``/``create_task`` must mark core params required."""
    tools = {t.name: t for t in await mcp_client.list_tools()}

    expectations = {
        "create_note": {"description", "related_to"},
        "log_meeting": {"title", "related_to"},
        "create_task": {"title"},
    }

    for tool_name, expected in expectations.items():
        assert tool_name in tools, f"{tool_name} not registered on server"
        schema = _input_schema(tools[tool_name])
        required = set(schema.get("required") or [])
        missing = expected - required
        assert not missing, (
            f"{tool_name} is missing required params {missing}; "
            f"declared required={sorted(required)}"
        )


async def test_entity_ref_schema_exposes_kind_enum(mcp_client):
    """``EntityRef.kind`` must surface as a JSON Schema enum on write tools.

    This is what turns ``kind`` into a dropdown in MCP clients instead of a
    free-text field where agents can hallucinate garbage values.
    """
    tools = {t.name: t for t in await mcp_client.list_tools()}

    for tool_name in ("create_note", "log_meeting"):
        assert tool_name in tools, f"{tool_name} not registered on server"
        schema = _input_schema(tools[tool_name])
        enum_values = _find_kind_enum(schema)
        assert enum_values is not None, (
            f"{tool_name}: could not find `kind` enum in inputSchema — "
            f"EntityRef may not be inlined correctly"
        )
        assert set(enum_values) == EXPECTED_RELATED_KINDS, (
            f"{tool_name}: kind enum {sorted(enum_values)} != "
            f"expected {sorted(EXPECTED_RELATED_KINDS)}"
        )
