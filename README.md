# Recruit CRM MCP

[![CI](https://github.com/ebragas/recruitcrm-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ebragas/recruitcrm-mcp/actions/workflows/ci.yml)

MCP (Model Context Protocol) server for [Recruit CRM](https://www.recruitcrm.io/), enabling AI assistants to search candidates, view jobs, and manage recruiting workflows.

## Quick Start

### One-Click Install (recommended)

Run this in your terminal — it handles everything automatically:

```bash
curl -LsSf https://raw.githubusercontent.com/ebragas/recruitcrm-mcp/main/install.sh | bash
```

Or download and review the script first:

```bash
curl -LsSf https://raw.githubusercontent.com/ebragas/recruitcrm-mcp/main/install.sh -o install.sh
cat install.sh   # review the script
bash install.sh
```

The installer will:
- Install `uv` if you don't have it
- Prompt for your Recruit CRM API key
- Back up your existing Claude Desktop config
- Add the Recruit CRM MCP server entry

> Already have `uv`? You can skip the bootstrap and run the installer directly:
> ```bash
> uvx --from recruit-crm-mcp recruit-crm-mcp-install
> ```

### Manual Setup

If you prefer to configure manually, add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "recruit-crm": {
      "command": "uvx",
      "args": ["recruit-crm-mcp"],
      "env": {
        "RECRUIT_CRM_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Development

```bash
uv sync              # install dependencies
make test            # run tests
make lint            # run linter
make check           # run lint + tests
```

## Tools

| Tool | Description |
|------|-------------|
| `ping` | Health check — verify the server is running and API key is configured |
| `find_candidates` | Find candidates — search with filters or list all |
| `get_candidate` | Get full profile details for a candidate by slug/ID |
| `list_jobs` | List job requisitions, optionally filtered by status |
| `get_job` | Get full details for a job by slug/ID |

## Resources

| Resource | Description |
|----------|-------------|
| `recruitcrm://candidate/{id}/resume` | Get resume URL for a candidate |
| `recruitcrm://job/{id}/description` | Get full job description |

## Configuration

Set the `RECRUIT_CRM_API_KEY` environment variable with your Recruit CRM API token.
