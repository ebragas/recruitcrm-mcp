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
| `GET /jobs/{slug}/assigned-candidates` | Candidates assigned to a job |
| `GET /contacts` | Contacts list |
| `GET /contacts/search` | Search contacts |
| `GET /contacts/{slug}` | Contact by slug |
| `GET /users` | List team members/users |
| `GET /companies` | Companies list |
| `GET /companies/search` | Search companies |
| `GET /companies/{slug}` | Company by slug |
| `GET /notes` | Notes list |
| `GET /notes/search` | Search notes |
| `GET /notes/{id}` | Note by ID |
| `GET /tasks` | Tasks list |
| `GET /tasks/search` | Search tasks |
| `GET /tasks/{id}` | Task by ID |
| `GET /meetings` | Meetings list |
| `GET /meetings/search` | Search meetings |
| `GET /meetings/{id}` | Meeting by ID |

### Field Mapping Gotchas

- Candidate company → `current_organization` (not `company_name`)
- Candidate job title → `position` (primary populated field)
- Candidate resume → object: `{"filename": "...", "file_link": "..."}`
- Job status → `job_status` object: `{"id": 1, "label": "Open"}`
- Job description → `job_description_text` (HTML)
- Pagination: `/candidates` uses `limit` param; `/jobs` uses `per_page` (min 15/page, below minimum is ignored)
- `/candidates/search` supports: `first_name`, `last_name`, `email`, `linkedin`, `contact_number`, `state`, `country`, `created_from/to`, `updated_from/to` — does NOT support `per_page`, `search`, `city`, `job_title`, `sort_by`, or `sort_order`
- `/candidates` list endpoint only accepts `limit` — rejects `sort_by`/`sort_order` with 422 (despite docs listing them)
- **sort_by/sort_order:** The API docs list these as supported on candidate endpoints, but the live API rejects them with 422 on both `/candidates` and `/candidates/search`. Do not add these params without first verifying via integration test.
- **Country filter uses fuzzy matching:** Searching `country=United States` also returns candidates with `country=United States of America`. State filter uses exact matching.
- `/jobs/search` rejects `per_page` with 400
- `/jobs/search` supports: `created_from`, `created_to`, `updated_from`, `updated_to`, `owner_id` — does NOT accept `created_on`, `updated_on`, or `owner` (400 rejected)
- Job salary fields use `min_annual_salary`/`max_annual_salary` (not `minimum_`/`maximum_` prefix)
- `job_location_type` is a string: `"0"`=On-site, `"1"`=Remote, `"2"`=Hybrid
- `owner` field on jobs is an integer user ID — use `/users` endpoint to resolve to names
- `/contacts/search` supports: `first_name`, `last_name`, `email`, `linkedin`, `contact_number`, `company_slug`, `created_from/to`, `updated_from/to`, `owner_id` — does NOT accept `designation` (400 rejected)
- `/contacts` list endpoint accepts `limit` param
- Search endpoints return `[]` when called with no filter params
- "Closed" job status has ID `0`, which the API treats as no-filter — closed jobs cannot be filtered via `/jobs/search`
- `/companies/search` supports: `company_name`, `created_from/to`, `updated_from/to`, `owner_id`, `owner_name`, `owner_email`, `sort_by`, `sort_order`, `exact_search`, `marked_as_off_limit`
- `/companies/search` `sort_by` accepts `createdon` or `updatedon`; `sort_order` accepts `asc` or `desc`
- `/companies/search` `exact_search` toggles exact vs fuzzy name matching (default is fuzzy/like)
- `/companies` list endpoint accepts `limit` param
- `/companies/search` returns `[]` with no filter params
- Companies are referenced by `slug` — jobs reference companies via `company_slug`
- Notes use `id` (integer) not `slug` — `GET /notes/{id}`
- `/notes/search` supports: `added_from/to`, `updated_from/to` — does NOT accept `created_from/to` (400 rejected), `related_to` or `related_to_type` (422 rejected)
- `/notes/search` uses `added_from`/`added_to` instead of `created_from`/`created_to` (unique naming)
- `/notes` list endpoint accepts `limit` param
- `/notes/search` returns `[]` with no filter params
- Note `note_type` is an object: `{"id": 48622, "label": "Note"}`
- Tasks use `id` (integer) not `slug` — `GET /tasks/{id}`
- `/tasks/search` supports: `title`, `created_from/to`, `updated_from/to`, `starting_from/to`, `owner_id` — does NOT accept `related_to` or `related_to_type` (422 rejected)
- `/tasks` list endpoint accepts `limit` param
- `/tasks/search` returns `[]` with no filter params
- Task `task_type` can be null or an object: `{"id": 1, "label": "Call"}`
- Meetings use `id` (integer) not `slug` — `GET /meetings/{id}`
- Meeting `meeting_type` is an object: `{"id": 40014, "label": "Candidate Interview"}`
- Meeting `status` is an integer (not an object like job_status)
- `/meetings/search` supports: `title`, `created_from/to`, `updated_from/to`, `starting_from/to`, `owner_id` — does NOT accept `related_to` or `related_to_type` (422 rejected)
- `/meetings` list endpoint accepts `limit` param
- `/meetings/search` returns `[]` with no filter params
- **Custom fields are inline on update, not a sub-endpoint.** `POST /companies/{slug}`, `POST /contacts/{slug}`, `POST /jobs/{slug}`, `POST /candidates/{slug}` all accept `custom_fields: [{field_id, value}]` inline in the body. There is NO `/associated-fields` sub-endpoint for company/contact/candidate — that path exists only for candidate-on-job application-question answers, which is out of scope.
- **Job create required fields (seven):** `name`, `number_of_openings`, `company_slug`, `contact_slug`, `job_description_text`, `currency_id`, `enable_job_application_form`. Omit any of these and the API 422s.
- **Assign / unassign use `job_slug` as a QUERY PARAM, not a body field.** `POST /candidates/{slug}/assign?job_slug=...` and `POST /candidates/{slug}/unassign?job_slug=...`. No body.
- **Hiring stage update path uses both slugs and the plural segment:** `POST /candidates/{candidate_slug}/hiring-stages/{job_slug}` with body `{status_id, remark?, stage_date?, create_placement?}`.
- **File upload uses one endpoint for every entity type.** `POST /v1/files` with multipart form fields `related_to`, `related_to_type`, `folder`, and `files[]`. `files[]` accepts a public URL string OR a file — we support URLs in the MCP. There is no DELETE /files endpoint.
- **Contact multi-company uses comma-separated `company_slug`.** On `POST /contacts` / `POST /contacts/{slug}`, pass `"slug1,slug2"` as the `company_slug` field. The read response returns `company_slug` (primary) and `additional_company_slugs` (others) separately, but writes expect one combined comma-separated string.
- **Hiring pipeline stages key mismatch:** `GET /hiring-pipelines/{id}` returns items shaped `{status_id, label}` despite API docs claiming `stage_id`. Code must read `status_id`. `/sales-pipeline` correctly returns `stage_id` as documented.
- **All `update_*` endpoints accept true partial POST.** Per each `edit-*.md`, every body field is optional; the live API confirms this for `/companies/{slug}`, `/contacts/{slug}`, `/candidates/{slug}`, `/jobs/{slug}`, `/meetings/{id}`, and `/tasks/{id}`. Send only fields you want to change; omitted fields are preserved server-side.
- **Do not fetch-merge-POST on update endpoints.** The read shape diverges from the write shape (nested `task_type`/`meeting_type` vs scalar `*_type_id`; array `associated_*` vs comma-separated string; string `owner` vs integer `owner_id`) — re-posting the GET body yields 422 on every associated field.
- **Task `status` is NOT writable via any public endpoint.** The edit-task.md write body omits `status`; sending it returns 200 but the API silently ignores it. Probed every plausible field name (`status`, `is_complete`, `completed`, `mark_complete`, `task_status`, `task_status_id`, `is_done` — across int/string/bool shapes on 2026-04-24) — all silently ignored, `status` stays at `0`. No dedicated task-completion endpoint exists in `docs/api-reference/`. Clients needing this must either delete the task or use the Recruit CRM UI. Treat as a product gap; file a vendor request if needed.
- **`do_not_send_calendar_invites` rejects JSON `false` with 422.** The API accepts Python `True`, `"1"`, `"0"`, `0`, `1` — but `False` triggers `"The selected do not send calendar invites is invalid."` Server code must serialize bool to `"1"`/`"0"` strings before POSTing.
- **`/jobs` create requires a lot:** `name`, `number_of_openings`, `company_slug`, `contact_slug`, `currency_id`, `job_description_text`, and `enable_job_application_form` — heavy enough that inline test fixtures for jobs aren't cheap.
- **`/jobs` create also requires contact/company linkage:** the `contact_slug` must be linked to the same `company_slug` at contact-creation time (pass `company_slug` on `POST /contacts`). Otherwise `POST /jobs` returns 422 `contact_slug should be linked with provided company_slug`. This constraint is undocumented.
- **Meeting attendees asymmetric on read vs write:** `POST /meetings` takes `attendee_candidates`/`attendee_contacts`/`attendee_users` as comma-separated slug strings. `GET /meetings/{id}` does NOT echo those fields — returns `None` for them. Attendees instead appear under a separate `attendees: [{attendee_id, attendee_type, display_name}]` list with `attendee_type` discriminating `"Candidate"`/`"Contact"`/`"User"`.

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

### Commit Messages

- **Never** add `Co-Authored-By: Claude` or any similar co-author attribution to commit messages, code comments, or anywhere in the codebase.

### Workflow

1. Create branch with issue ID (e.g., `MAIN-73/scaffold-mcp`) — from `main` or parent feature branch
2. Transition the Linear issue to "In Progress"
3. Comment on the Linear issue that work is starting
4. Implement, run `make check` to verify
5. Check off completed subtasks on the Linear issue description
6. Use `/commit-commands:commit-push-pr` to commit, push, and open a PR
7. Request Copilot review: `gh api repos/ebragas/recruitcrm-mcp/pulls/<PR_NUMBER>/requested_reviewers --method POST -f 'reviewers[]=Copilot'`
8. Transition the Linear issue to "In Review"

### Test-Driven API Development

**Never assume an API parameter works based on documentation alone.** The Recruit CRM API docs have listed parameters that the live API rejects (e.g. `sort_by`/`sort_order`). When adding new API parameters:

1. **Write an integration test first** that calls the live API with the new parameter and asserts expected behavior (correct filtering, field values, status codes).
2. **Run the integration test** (`make integration-test`) to confirm the API actually accepts the parameter.
3. **Only then** add the parameter to client/server code and write unit tests.
4. **Include a "rejection guard" integration test** for params the API is known to reject — these prevent regressions if the API behavior changes later.

### Linear Integration

- Agent ID: `claude-code-recruitcrm-mcp`
- **Linear project:** `Build Recruit CRM MCP` — always include `--project "Build Recruit CRM MCP"` when creating issues
- Comment on issues when starting and completing work
- Transition issues through: Todo → In Progress → In Review → Done
- Valid states: Backlog, Todo, In Progress, In Review, Done, Canceled, Duplicate

### Pre-release workflow

Pre-release builds (`X.Y.ZrcN`, `X.Y.ZaN`, `X.Y.ZbN`, `X.Y.Z.devN`) are published manually for internal testing. They do NOT affect the stable release line driven by semantic-release on `main`.

To cut a pre-release:

1. Push the branch you want to ship (any branch works).
2. GitHub Actions → **Publish pre-release** → Run workflow → pick the branch → enter the version (e.g. `0.16.0rc1`). The workflow validates the version is a PEP 440 pre-release, runs lint + unit tests, then publishes to PyPI via the existing `pypi` trusted-publisher environment. The version pin happens only on the runner — `pyproject.toml` on the branch is unchanged.
3. Consumers install with an explicit pin (see README "Installing a pre-release (test) build").

The unpinned `uvx recruit-crm-mcp` in the standard installer keeps resolving to the latest stable — pre-releases are invisible unless pinned, because uv's default `--prerelease=if-necessary` strategy skips them when a stable satisfies the spec.

The workflow trigger is `workflow_dispatch` only. No push, tag, or PR merge can cut a pre-release.
