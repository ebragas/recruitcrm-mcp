import os
from importlib.metadata import version, PackageNotFoundError

from fastmcp import FastMCP

try:
    __version__ = version("recruit-crm-mcp")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

mcp = FastMCP("Recruit CRM")


@mcp.tool()
def ping() -> dict:
    """Check that the Recruit CRM MCP server is running and configured."""
    has_key = bool(os.environ.get("RECRUIT_CRM_API_KEY"))
    return {
        "status": "ok",
        "version": __version__,
        "api_configured": has_key,
    }


def main():
    mcp.run()


if __name__ == "__main__":
    main()
