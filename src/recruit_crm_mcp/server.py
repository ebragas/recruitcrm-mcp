import os

from fastmcp import FastMCP

mcp = FastMCP("Recruit CRM")

API_BASE = "https://api.recruitcrm.io/v1"


def _get_api_key() -> str:
    key = os.environ.get("RECRUIT_CRM_API_KEY")
    if not key:
        raise RuntimeError("RECRUIT_CRM_API_KEY environment variable is required")
    return key


@mcp.tool()
def ping() -> dict:
    """Check that the Recruit CRM MCP server is running and configured."""
    has_key = bool(os.environ.get("RECRUIT_CRM_API_KEY"))
    return {
        "status": "ok",
        "version": "0.1.0",
        "api_configured": has_key,
    }


def main():
    mcp.run()


if __name__ == "__main__":
    main()
