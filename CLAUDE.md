# Recruit CRM MCP

## Project Overview

MCP (Model Context Protocol) server for Recruit CRM, built with Python and FastMCP. Distributed via PyPI for zero-touch updates using `uvx`.

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastMCP
- **HTTP Client:** httpx
- **Package Manager:** uv
- **Distribution:** PyPI via `uvx`

## Development Setup

```bash
uv sync          # install dependencies and create venv
uv run <cmd>     # run commands in the venv
```

## Conventions

### Git Branching

- Branch from `main`
- Branch naming: `<issue-id>/<short-description>` (e.g., `MAIN-73/scaffold-mcp`)
- Linear auto-tracks branches with issue IDs in the name

### Code Style

- Source layout: `src/recruit_crm_mcp/`
- Keep tools focused — one tool per logical API operation
- API key via `RECRUIT_CRM_API_KEY` environment variable

### Workflow

1. Create branch from `main` with issue ID (e.g., `MAIN-73/scaffold-mcp`)
2. Comment on the Linear issue that work is starting
3. Implement, run `make check` to verify
4. Check off completed subtasks on the Linear issue description
5. Use `/commit-commands:commit-push-pr` to commit, push, and open a PR
6. Transition the Linear issue to "In Review"

### Linear Integration

- Agent ID: `claude-code-recruitcrm-mcp`
- Comment on issues when starting and completing work
- Transition issues through: Todo → In Progress → In Review → Done
- Valid states: Backlog, Todo, In Progress, In Review, Done, Canceled, Duplicate
