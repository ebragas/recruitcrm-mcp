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

## Recruit CRM API Reference

- **Base URL:** `https://api.recruitcrm.io/v1`
- **Auth:** `Authorization: Bearer <RECRUIT_CRM_API_KEY>`
- **Rate limit:** 60 requests/minute (<6 licenses)
- **Docs:** https://docs.recruitcrm.io/docs/rcrm-api-reference/9033e3227d21f-recruit-crm-api

### Key Endpoints

| Endpoint | Docs |
|---|---|
| `GET /candidates` | [Search candidates](https://docs.recruitcrm.io/docs/rcrm-api-reference/253721386feef-search-for-candidates) |
| `GET /candidates/{slug}` | [Find by slug](https://docs.recruitcrm.io/docs/rcrm-api-reference/6de2e46e80e6a-find-candidate-by-slug) |
| `GET /jobs` | Jobs list |
| `GET /jobs/{slug}` | Job by slug |

### Field Mapping Gotchas

- Candidate company → `current_organization` (not `company_name`)
- Candidate job title → `position` (primary populated field)
- Candidate resume → object: `{"filename": "...", "file_link": "..."}`
- Job status → `job_status` object: `{"id": 1, "label": "Open"}`
- Job description → `job_description_text` (HTML)
- Pagination: candidates min 100/page, jobs min 15/page — `per_page` below minimums is ignored
- Search endpoints (`/candidates/search`, `/jobs/search`) reject `per_page` with 400 — use `limit` or omit and enforce client-side
- Search endpoints return `[]` when called with no filter params
- "Closed" job status has ID `0`, which the API treats as no-filter — closed jobs cannot be filtered via `/jobs/search`

### Concurrency

- **"Sibling tool call errored"** is a Claude Code client-side behavior, not a server bug. When one tool call in a parallel batch fails, Claude Code cancels the remaining siblings. The fix is to ensure tools don't error — not to handle concurrency differently.
- FastMCP dispatches each incoming `tools/call` as a concurrent async task via `anyio.create_task_group`
- `httpx.AsyncClient` is safe for concurrent async use within a single event loop
- The shared `_client` is eagerly initialized once in the lifespan handler (via `init_client()`), then reused across requests; `httpx.AsyncClient` is safe for concurrent async use within a single event loop

## Conventions

### Git Branching

- Branch from `main` or parent feature branch for sequential work
- Branch naming: `<issue-id>/<short-description>` (e.g., `MAIN-73/scaffold-mcp`)
- Linear auto-tracks branches with issue IDs in the name
- **Sequential issue chains:** When working multiple issues in sequence, branch each new issue off the previous issue's branch (not `main`). Set the parent branch as the PR base (`gh pr create --base <parent-branch>`) so each PR's diff only shows the new work. Link the parent PR in the description if helpful.
- **PR titles must include the Linear issue ID** (e.g., `MAIN-87: fix jobs status filter`)

### Code Style

- Source layout: `src/recruit_crm_mcp/`
- Keep tools focused — one tool per logical API operation
- API key via `RECRUIT_CRM_API_KEY` environment variable
- **No backward compatibility shims.** This is an MCP server, not a library — there are no external callers. When signatures change, update all internal call sites and delete the old code. Don't add deprecation wrappers or keep dead parameters around.

### Workflow

1. Create branch with issue ID (e.g., `MAIN-73/scaffold-mcp`) — from `main` or parent feature branch
2. Transition the Linear issue to "In Progress"
3. Comment on the Linear issue that work is starting
4. Implement, run `make check` to verify
5. Check off completed subtasks on the Linear issue description
6. Use `/commit-commands:commit-push-pr` to commit, push, and open a PR
7. Transition the Linear issue to "In Review"

### Linear Integration

- Agent ID: `claude-code-recruitcrm-mcp`
- **Linear project:** `Build Recruit CRM MCP` — always include `--project "Build Recruit CRM MCP"` when creating issues
- Comment on issues when starting and completing work
- Transition issues through: Todo → In Progress → In Review → Done
- Valid states: Backlog, Todo, In Progress, In Review, Done, Canceled, Duplicate
