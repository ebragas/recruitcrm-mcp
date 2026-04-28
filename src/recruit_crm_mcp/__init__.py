"""MCP server for Recruit CRM."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("recruit-crm-mcp")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
