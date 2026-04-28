# Recruit CRM MCP

[![CI](https://github.com/ebragas/recruitcrm-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ebragas/recruitcrm-mcp/actions/workflows/ci.yml)

MCP (Model Context Protocol) server for [Recruit CRM](https://www.recruitcrm.io/), enabling AI assistants to search candidates, view jobs, and manage recruiting workflows.

## Quick Start

### One-Click Install (recommended)

**macOS / Linux** — run in Terminal:

```bash
curl -LsSf https://raw.githubusercontent.com/ebragas/recruitcrm-mcp/main/install.sh | bash
```

**Windows** — run in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://raw.githubusercontent.com/ebragas/recruitcrm-mcp/main/install.ps1 | iex"
```

The installer will:
- Install `uv` if you don't have it
- Prompt for your Recruit CRM API key
- Back up your existing Claude Desktop config
- Add the Recruit CRM MCP server entry

<details>
<summary>Want to review the script first?</summary>

**macOS / Linux:**

```bash
curl -LsSf https://raw.githubusercontent.com/ebragas/recruitcrm-mcp/main/install.sh -o install.sh
cat install.sh   # review the script
bash install.sh
```

**Windows:**

```powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/ebragas/recruitcrm-mcp/main/install.ps1 -OutFile install.ps1
Get-Content install.ps1   # review the script
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

</details>

> Already have `uv`? You can skip the bootstrap and run the installer directly:
> ```
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

### Installing a pre-release (test) build

Pre-release builds (e.g. `0.16.0rc1`) are published to PyPI for internal
testing. They are **not** picked up by the default installer or by a bare
`uvx recruit-crm-mcp` — you have to pin them explicitly.

To run a pre-release once from the command line:

```bash
uvx recruit-crm-mcp@0.16.0rc1
```

To use a pre-release with Claude Desktop, edit `claude_desktop_config.json`
and change the `args` entry to include the version pin:

```json
{
  "mcpServers": {
    "recruit-crm": {
      "command": "uvx",
      "args": ["recruit-crm-mcp@0.16.0rc1"],
      "env": {
        "RECRUIT_CRM_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Fully quit and reopen Claude Desktop (the app keeps running in the dock
after closing the window).

**To roll back to stable**, set `args` back to `["recruit-crm-mcp"]` (or
pin a specific stable like `["recruit-crm-mcp@0.15.0"]`) and restart
Claude Desktop.

> **Why other users are safe.** `uvx`'s default resolver strategy is
> `--prerelease=if-necessary`: pre-releases are skipped unless no stable
> version satisfies the spec. Because `recruit-crm-mcp` has a stable
> release on PyPI, the unpinned `uvx recruit-crm-mcp` in the default
> installer's config resolves to the latest stable and never picks up a
> pre-release. Only an explicit pin like `@0.16.0rc1` opts in.

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

### Candidates

| Tool | Description |
|------|-------------|
| `search_candidates` | Search candidates by name, email, LinkedIn, phone, state, country, or created/updated date range |
| `get_candidate` | Get full profile details for a candidate by slug/ID |
| `create_candidate` | Create a new candidate record |
| `update_candidate` | Update standard fields on an existing candidate |
| `set_candidate_custom_fields` | Set custom-field values on a candidate without touching standard fields |

### Jobs

| Tool | Description |
|------|-------------|
| `list_jobs` | List job requisitions in reverse chronological order |
| `search_jobs` | Search jobs by status, name, city, country, company, owner, or created/updated date range |
| `get_job` | Get full details for a job by slug/ID |
| `create_job` | Create a new job requisition (requires name, openings, company_slug, contact_slug, description, currency, application form flag) |
| `update_job` | Update standard fields on an existing job |
| `set_job_custom_fields` | Set custom-field values on a job without touching standard fields |
| `get_assigned_candidates` | List candidates assigned to a job (optionally filtered by hiring stage) |

### Contacts

| Tool | Description |
|------|-------------|
| `search_contacts` | Search contacts by name, email, LinkedIn, phone, company_slug, owner, or date range |
| `get_contact` | Get full details for a contact by slug |
| `create_contact` | Create a new contact record |
| `update_contact` | Update standard fields on an existing contact |
| `set_contact_custom_fields` | Set custom-field values on a contact without touching standard fields |

### Companies

| Tool | Description |
|------|-------------|
| `search_companies` | Search companies by name, owner, off-limit flag, or date range (supports sort and exact match) |
| `get_company` | Get full details for a company by slug |
| `create_company` | Create a new company record |
| `update_company` | Update standard fields on an existing company |
| `set_company_custom_fields` | Set custom-field values on a company without touching standard fields |

### Notes / Tasks / Meetings

| Tool | Description |
|------|-------------|
| `search_notes` | Search notes by `added_from/to` and `updated_from/to` |
| `get_note` | Get a note by ID |
| `create_note` | Create a note attached to a candidate, job, contact, or company |
| `delete_note` | Delete a note by ID |
| `search_tasks` | Search tasks by title, owner, and created/updated/starting date ranges |
| `get_task` | Get a task by ID |
| `create_task` | Create a task attached to a related entity, with optional reminder |
| `update_task` | Update fields on an existing task |
| `search_meetings` | Search meetings by title, owner, and created/updated/starting date ranges |
| `get_meeting` | Get a meeting by ID |
| `log_meeting` | Log (create) a meeting against a related entity with attendees and timing |
| `update_meeting` | Update fields on an existing meeting |

### Assignments

| Tool | Description |
|------|-------------|
| `assign_candidate` | Assign a candidate to a job |
| `unassign_candidate` | Remove a candidate-job assignment |
| `update_hiring_stage` | Move a candidate's hiring stage on a job |

### Files

| Tool | Description |
|------|-------------|
| `upload_file` | Attach a public-URL file to a candidate, company, contact, or job |

### Users / Lookups

| Tool | Description |
|------|-------------|
| `list_users` | List team members/users |
| `list_note_types` | Enumerate note type IDs and labels |
| `list_meeting_types` | Enumerate meeting type IDs and labels |
| `list_task_types` | Enumerate task type IDs and labels |
| `list_hiring_pipelines` | List hiring pipelines configured in the account |
| `list_hiring_pipeline_stages` | Stages for a hiring pipeline (pipeline_id=0 = master) |
| `list_contact_stages` | List sales pipeline stages (contact stages) |
| `list_industries` | List industries available in the account |
| `list_company_custom_fields` | Custom-field definitions for companies |
| `list_contact_custom_fields` | Custom-field definitions for contacts |
| `list_job_custom_fields` | Custom-field definitions for jobs |
| `list_candidate_custom_fields` | Custom-field definitions for candidates |

### Feedback

| Tool | Description |
|------|-------------|
| `report_issue` | Build a prefilled GitHub Issues URL the user can click to file a bug report |

## Resources

| Resource | Description |
|----------|-------------|
| `recruitcrm://candidate/{id}/resume` | Get resume URL for a candidate |
| `recruitcrm://job/{id}/description` | Get full job description |

## Configuration

Set environment variables in your MCP client config (e.g. `claude_desktop_config.json`'s `env` block):

| Var | Required | Default | Description |
|---|---|---|---|
| `RECRUIT_CRM_API_KEY` | yes | — | Recruit CRM API token. |
| `RECRUIT_CRM_MCP_SENTRY_DSN` | no | unset | Your own Sentry project DSN. If set, tool-call exceptions are auto-reported to that project. See [Error reporting](#error-reporting) below. |
| `SENTRY_DSN` | no | unset | Fallback DSN if you already export it globally. `RECRUIT_CRM_MCP_SENTRY_DSN` takes precedence. |
| `RECRUIT_CRM_MCP_ENV` | no | `production` | Sentry environment tag. |
| `RECRUIT_CRM_MCP_SENTRY_TRACES_RATE` | no | `0.0` | Sentry trace sample rate (0.0–1.0). |

## Error reporting

Two complementary, fully optional channels for surfacing problems:

### 1. `report_issue` MCP tool (always available)

When something goes wrong and you want to send a structured bug report, ask Claude to "report this issue" or "file a bug." The MCP exposes a `report_issue` tool that builds a prefilled GitHub Issues URL — Claude returns the link, you click it, GitHub opens the new-issue form pre-populated with the summary, the last error, and your environment details. Submit it from your browser like any other issue. Works with any GitHub account; no token in the MCP, no collaborator access needed, repo is public.

### 2. Sentry auto-capture (bring-your-own-DSN)

If you want passive observability — every tool-call exception captured automatically with stack trace, span context, and HTTP breadcrumbs — set `RECRUIT_CRM_MCP_SENTRY_DSN` to a Sentry project DSN that you control. With no DSN set (the default), the MCP makes zero network calls to Sentry.

This is **strictly bring-your-own-DSN**. We do not publish or embed a project DSN. If you want this, sign up for a free Sentry account, create a Python project, copy its DSN, and put it in your MCP client config:

```json
{
  "mcpServers": {
    "recruit-crm": {
      "command": "uvx",
      "args": ["recruit-crm-mcp"],
      "env": {
        "RECRUIT_CRM_API_KEY": "...",
        "RECRUIT_CRM_MCP_SENTRY_DSN": "https://<key>@<org>.ingest.sentry.io/<project>"
      }
    }
  }
}
```

When enabled, the following ends up in *your* Sentry project: tool name, exception type and stack trace, tool arguments and return values (via `MCPIntegration(include_prompts=True)`), HTTPX breadcrumbs (URLs and status codes), MCP request/session IDs, and the package version. Recruit CRM data flowing through tools (candidate names, emails, company info) will appear in event payloads — that is the point, since most exceptions are unhelpful without the data that triggered them. Because the DSN is yours, the data only goes to your Sentry project.

## Privacy

- **No telemetry by default.** With no Sentry DSN configured, the MCP makes zero network calls to anyone except `api.recruitcrm.io`.
- **No DSN is bundled.** We do not embed our own Sentry DSN — Sentry capture only works if you supply your own.
- **`report_issue` is explicit-consent.** It only builds a clickable URL; nothing is sent until you submit the prefilled form in your browser.
- **Public repo issues.** Reports filed via `report_issue` are publicly visible on GitHub. Don't paste secrets or PII you wouldn't want public.
