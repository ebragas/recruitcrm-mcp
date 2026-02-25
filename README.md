# Recruit CRM MCP

MCP (Model Context Protocol) server for [Recruit CRM](https://www.recruitcrm.io/), enabling AI assistants to search candidates, view jobs, and manage recruiting workflows.

## Quick Start

### With Claude Desktop (zero-touch via uvx)

Add to your `claude_desktop_config.json`:

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

## Configuration

Set the `RECRUIT_CRM_API_KEY` environment variable with your Recruit CRM API token.
