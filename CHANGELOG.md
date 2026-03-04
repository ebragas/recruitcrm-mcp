# CHANGELOG


## v0.12.0 (2026-03-04)

### Features

- Add search_notes tool with ID short-circuit
  ([`a624b27`](https://github.com/ebragas/recruitcrm-mcp/commit/a624b27c787a951a76bd6d21a8cfbfd7642e593f))

Add search_notes MCP tool for searching and listing notes in Recruit CRM. Notes use integer `id`
  (not `slug`). The API uses `added_from/to` instead of `created_from/to` — the tool maps
  `created_from/to` params to `added_from/to` internally for a consistent user interface. API
  rejects related_to, related_to_type (422), and created_from (400).

Includes integration tests (8 raw API probes + 4 client-level), unit tests, client methods
  (search_notes, get_note), _summarize_note, and CLAUDE.md endpoint/gotcha documentation.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>


## v0.11.0 (2026-03-04)

### Bug Fixes

- Correct test docstrings for filtered search tests
  ([`1e99bdc`](https://github.com/ebragas/recruitcrm-mcp/commit/1e99bdc3dfbe1363dec1172cea742b9b37d87811))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Chores

- **release**: 0.11.0
  ([`25e2cc3`](https://github.com/ebragas/recruitcrm-mcp/commit/25e2cc369e04a3378ae0726355d394574eb22fbf))


## v0.10.0 (2026-03-04)

### Bug Fixes

- Rename get_contact param to contact_slug and handle null names
  ([`aca575c`](https://github.com/ebragas/recruitcrm-mcp/commit/aca575cdb7884b9253ef54603506e896a2034c7b))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Split search_contacts into get_contact + search_contacts
  ([`f7f7b73`](https://github.com/ebragas/recruitcrm-mcp/commit/f7f7b734b5ba4ef0a405b2c646a23a4021a8f246))

Extract a dedicated get_contact tool so each tool has a consistent return type, matching the
  established get_*/search_* pattern.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Chores

- **release**: 0.10.0
  ([`295204d`](https://github.com/ebragas/recruitcrm-mcp/commit/295204dad5ce92375c8c22e8e747d1a98583f167))

### Testing

- Remove duplicate test_title_filter in meetings tests
  ([`a93d497`](https://github.com/ebragas/recruitcrm-mcp/commit/a93d49768fc4620768254d8f9b71ced5b88374d5))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Split get_meeting test from search_meetings tests
  ([`7997199`](https://github.com/ebragas/recruitcrm-mcp/commit/799719976e2c4601bc038ee3da604c7473fa250d))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>


## v0.9.0 (2026-03-03)

### Chores

- **release**: 0.9.0
  ([`1386845`](https://github.com/ebragas/recruitcrm-mcp/commit/13868456ed91d61de261a2c0d0c1f888bd8258bb))


## v0.8.0 (2026-03-03)

### Bug Fixes

- Address PR review — clarify search_jobs docstring
  ([`965216c`](https://github.com/ebragas/recruitcrm-mcp/commit/965216cbc3cd33d2f05b3a636240cf7d40bff063))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Address PR review — test actual tool function via mocked client
  ([`d8c0dca`](https://github.com/ebragas/recruitcrm-mcp/commit/d8c0dca2a862c7c125c9ac1bb5740d0e6b928d13))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Address PR review — use _parse_dt in job date tests
  ([`bfac6ec`](https://github.com/ebragas/recruitcrm-mcp/commit/bfac6ecba603678da29bd4a380db57af39755e12))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Chores

- **release**: 0.8.0
  ([`2801772`](https://github.com/ebragas/recruitcrm-mcp/commit/2801772fbe56e4665c526863807dd7cb8395dbe6))

### Features

- Add search_companies tool with slug short-circuit
  ([`9568a48`](https://github.com/ebragas/recruitcrm-mcp/commit/9568a48205564f245d26ddad81eafe1de64cca99))

Add search_companies MCP tool for searching and listing companies in Recruit CRM. Companies use slug
  identifiers. All documented search params verified via integration tests: company_name,
  created_from/to, updated_from/to, owner_id, sort_by/sort_order, exact_search, marked_as_off_limit,
  owner_name, owner_email.

Includes integration tests (12 raw API probes + 4 client-level), unit tests, client methods
  (search_companies, get_company), _summarize_company, and CLAUDE.md endpoint/gotcha documentation.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Add search_contacts tool with slug short-circuit
  ([`d2eabb5`](https://github.com/ebragas/recruitcrm-mcp/commit/d2eabb5796e1758d118ea110449df4d22ad3cae8))

Add search_contacts MCP tool combining listing and searching contacts. When contact_slug is
  provided, short-circuits to return raw record. Otherwise searches via /contacts/search with
  filters or falls back to /contacts for no-filter listing. Integration tests discovered that
  designation filter is rejected (400) by the API.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Add search_meetings tool with ID short-circuit
  ([`154a83c`](https://github.com/ebragas/recruitcrm-mcp/commit/154a83cfd32a119ab7c0866a25ad457fae7702f4))

Add search_meetings MCP tool for searching and listing meetings in Recruit CRM. Meetings use integer
  `id` (not `slug`). Supported search params: title, created_from/to, updated_from/to,
  starting_from/to,

owner_id. API rejects related_to and related_to_type with 422.

Includes integration tests (raw API probes + client-level), unit tests, client methods
  (search_meetings, get_meeting), _summarize_meeting, and CLAUDE.md endpoint/gotcha documentation.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Add search_tasks tool with ID short-circuit
  ([`8830ded`](https://github.com/ebragas/recruitcrm-mcp/commit/8830ded6f8ed817dc30a2e8b3276f61fecd12097))

Add search_tasks MCP tool for searching and listing tasks in Recruit CRM. Tasks use integer `id`
  (not `slug`). Supported search params: title, created_from/to, updated_from/to, starting_from/to,
  owner_id. API rejects related_to and related_to_type with 422 (same as meetings).

Includes integration tests (10 raw API probes + 4 client-level), unit tests, client methods
  (search_tasks, get_task), _summarize_task, and CLAUDE.md endpoint/gotcha documentation.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>


## v0.7.0 (2026-03-03)

### Bug Fixes

- Address PR review — fix docstring and test flakiness
  ([`160850d`](https://github.com/ebragas/recruitcrm-mcp/commit/160850db076169e821f27da2fb4416279d769a90))

- Update search_jobs docstring: filters are optional, empty list with no filters (not a hard
  requirement) - Derive date filter cutoffs from existing data in integration tests instead of
  hardcoding, with pytest.skip on empty results

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Address PR review — fuzzy country assertion and flaky date test
  ([`2c86a18`](https://github.com/ebragas/recruitcrm-mcp/commit/2c86a18a1594385df65f1a718babb4f0a92beab4))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Address PR review — handle naive/Z timestamps in date tests
  ([`f90693e`](https://github.com/ebragas/recruitcrm-mcp/commit/f90693e301531ef1cba75f4e7b3c6da2c5348996))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Main-153 replace broken search_candidates query parameters
  ([`d833ba8`](https://github.com/ebragas/recruitcrm-mcp/commit/d833ba8053b11df33e95eec318fc2d562ff2e3ca))

Replace non-functional query/city/job_title params with first_name/last_name that the
  /candidates/search endpoint actually supports. Fix email filter to route to /candidates/search
  instead of /candidates. Remove per_page from search endpoint calls (causes 400). Add default
  sort_by=updated_at for the no-filter fallback path.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Remove vacuous assertion in test_returns_results
  ([`8090bd0`](https://github.com/ebragas/recruitcrm-mcp/commit/8090bd08f34dba29efdb8e364ef8f3764a70ec25))

The `assert len(results) > 0` inside `if results:` was always true.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Chores

- **release**: 0.7.0
  ([`5d98ad6`](https://github.com/ebragas/recruitcrm-mcp/commit/5d98ad6fecac6539c968f44fc15fb44e2aa53531))

### Continuous Integration

- Fix pypi-publish workflow using invalid dist-path input
  ([`2acc0bc`](https://github.com/ebragas/recruitcrm-mcp/commit/2acc0bc722104bad4e3a95e9ccf80c40cbe1a3cd))

MAIN-89: Replace `dist-path` with `packages-dir` in the pypa/gh-action-pypi-publish

step to eliminate the "Unexpected input" warning on every release run.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Features

- Main-151 add state, country, and date filters to search_candidates
  ([`eba78e2`](https://github.com/ebragas/recruitcrm-mcp/commit/eba78e24afc1d57bb2fb71e5ac4f2b4f5f27c551))

Add state, country, created_from, created_to, updated_from, updated_to params to search_candidates.
  Remove sort_by/sort_order which the live API rejects with 422 despite being listed in docs. Fix
  pre-existing 422 on the /candidates list fallback caused by hardcoded sort defaults.

Add integration tests verifying filter correctness (country, state, date range, combined filters)
  and rejection guard tests for sort params. Update CLAUDE.md with API gotchas and TDD workflow for
  new API params.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Main-155 expand search_jobs response fields, add date/owner filters and list_users tool
  ([`6710fd5`](https://github.com/ebragas/recruitcrm-mcp/commit/6710fd5c211b8dcc1201cd981f69fb6e6931b1a1))

Add 12 new fields to job summaries (salary, experience, location type, description, etc.), date
  range and owner_id filters to search_jobs, and a new list_users tool for discovering owner IDs.

Also fix pre-existing trio test failures by switching asyncio.sleep to anyio.sleep and restricting
  test backend to asyncio-only (removes trio dependency).

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Main-156 add get_assigned_candidates tool
  ([`cc9be8a`](https://github.com/ebragas/recruitcrm-mcp/commit/cc9be8a10e1775aec9ceecf2405d01822d3417b9))

Add tool to retrieve candidates assigned to a job with their hiring stage via GET
  /jobs/{slug}/assigned-candidates. Supports status_id filtering and client-side limit enforcement.
  Reuses _summarize_candidate for consistent output with search_candidates.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Refactoring

- Extract _extract_results helper, fix _job_location_label, remove description from job summary
  ([`b94637c`](https://github.com/ebragas/recruitcrm-mcp/commit/b94637c123845d187f48f20e4c6e175e22c094fa))

- Extract _extract_results() to deduplicate 4 identical response-parsing blocks in client.py - Fix
  _job_location_label None handling: replace str(None) accidental fallthrough with explicit guard -
  Remove job_description_text from _summarize_job — large HTML payloads belong in get_job/job
  description resource, not list/search summaries

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Testing

- Remove duplicate email filter test
  ([`37e04c3`](https://github.com/ebragas/recruitcrm-mcp/commit/37e04c323e4fac92b9e825727acdb8375822b034))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>


## v0.6.2 (2026-02-26)

### Bug Fixes

- **client**: Update search_candidates docstring to match behavior
  ([`ac76f91`](https://github.com/ebragas/recruitcrm-mcp/commit/ac76f912ebb5b4713e60cc0e589cafdd8bd5a29c))

Filters are optional, not required — align client docstring with the server docstring updated in the
  previous commit.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- **docs**: Address PR review comments on search/list tools
  ([`829a579`](https://github.com/ebragas/recruitcrm-mcp/commit/829a5793c6777e297abf3505c997b906dbcff7c2))

- Remove unverified "reverse chronological order" claim from list_candidates - Update
  search_candidates docstring to reflect actual behavior (no filters = empty list) - Guard
  integration test against falsy first_name

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- **search**: Don't send per_page to search endpoint, add list_candidates
  ([`7b394b2`](https://github.com/ebragas/recruitcrm-mcp/commit/7b394b2520497d570bee8aea932d54e53a9aabe5))

The /candidates/search endpoint rejects per_page with 400. It also returns [] with no filters, so a
  separate list_candidates function (hitting /candidates) is needed for unfiltered browsing.

Adds integration tests that confirm the MAIN-85 fix: filters actually narrow results, and different
  filters produce different result sets.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- **search**: Use correct API endpoint and params for candidate search
  ([`e5b740d`](https://github.com/ebragas/recruitcrm-mcp/commit/e5b740d5bd6475cc2a8a3208ae9a00d254a87f35))

search_candidates was hitting /candidates (list endpoint) for field filters, which silently ignores
  all filter params. Now always uses /candidates/search with the params the API actually supports:
  first_name, last_name, email, country, state.

Removes unsupported params (query, city, job_title) that never worked.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Chores

- Gitignore fetched API docs
  ([`7b2eebc`](https://github.com/ebragas/recruitcrm-mcp/commit/7b2eebcae07a2eae062a77473865729a2f69f123))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Merge main and reconcile remote branch
  ([`92bda65`](https://github.com/ebragas/recruitcrm-mcp/commit/92bda654e27eebac4b36a7cbcc9b6a03e8e2af22))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Merge main into MAIN-85/fix-candidate-search
  ([`c5e8067`](https://github.com/ebragas/recruitcrm-mcp/commit/c5e8067ffcd1eb8cc84fc833df562167c7cfa005))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- **release**: 0.6.2
  ([`6f4f73a`](https://github.com/ebragas/recruitcrm-mcp/commit/6f4f73a25583ad7c23e8663bc1dc1aca7c438d75))

### Documentation

- Update CLAUDE.md to reflect eager client init pattern
  ([`66cebbf`](https://github.com/ebragas/recruitcrm-mcp/commit/66cebbfc98f9fc21cce0d329d16a243fd9520c31))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Update README tools table for new search params
  ([`d2e7c1d`](https://github.com/ebragas/recruitcrm-mcp/commit/d2e7c1dd13f292352423ef4f17c254814b69c8a0))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Refactoring

- Merge list_jobs into find_jobs with dynamic status resolution
  ([`8b78b3e`](https://github.com/ebragas/recruitcrm-mcp/commit/8b78b3e83ea25138ceb907ffca6b18a00ca10fcf))

Replace list_jobs with find_jobs using the same pattern as find_candidates: filters present →
  /jobs/search, no filters → /jobs.

New filters: name, status, city, country, company_name. Status labels (e.g. "Open", "On Hold") are
  resolved to API integer IDs via /jobs-pipeline, cached for the session. Closed status (ID 0)
  returns a clear error since the API treats it as no-filter.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- Merge search_candidates and list_candidates into find_candidates
  ([`22404b7`](https://github.com/ebragas/recruitcrm-mcp/commit/22404b769879d4c629528f9827ac124eef5d1165))

Single tool that routes internally: filters present → /candidates/search, no filters → /candidates.
  Simpler agent UX — one intent, one tool.

Also extracts _extract_results helper to DRY up response parsing.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- **client**: Eagerly init httpx client, document sibling error
  ([`ce0f3f5`](https://github.com/ebragas/recruitcrm-mcp/commit/ce0f3f53d84d35d07fafb7080782eb6aba37c138))

"Sibling tool call errored" is a Claude Code client-side behavior — when one parallel tool call
  fails, Claude Code cancels the siblings. The root cause was the broken filters in MAIN-85/MAIN-87
  causing tool errors that cascaded. No server concurrency bug exists.

Eagerly initializes the httpx AsyncClient in the server lifespan handler instead of lazy-init,
  making the lifecycle explicit.

Documents API quirks and concurrency notes in CLAUDE.md.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>


## v0.6.1 (2026-02-26)

### Chores

- Merge main into MAIN-87/fix-jobs-status-filter
  ([`ae2e976`](https://github.com/ebragas/recruitcrm-mcp/commit/ae2e976b29e34a03bf33a39314cd0bf68b34640c))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- **release**: 0.6.1
  ([`d6223b7`](https://github.com/ebragas/recruitcrm-mcp/commit/d6223b73fb6d7735be3e0d60d80854a93d6159e2))


## v0.6.0 (2026-02-26)

### Bug Fixes

- **jobs**: Use /jobs/search with job_status param for status filtering
  ([`6fb484e`](https://github.com/ebragas/recruitcrm-mcp/commit/6fb484e85b6be63d52d4a150ad4ff0464f55faec))

list_jobs was hitting /jobs which silently ignores filter params. Now split into list_jobs
  (unfiltered browse via /jobs) and search_jobs (filtered search via /jobs/search with job_status,
  name, city, country, company_name).

Status labels (Open, Closed, etc.) are mapped to the integer IDs the API expects. Note: "Closed" (ID
  0) is unsearchable due to an API quirk where 0 is treated as no-filter.

Also adds no-backward-compat convention to CLAUDE.md and gitignores fetched API docs.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Chores

- **release**: 0.6.0
  ([`424da7a`](https://github.com/ebragas/recruitcrm-mcp/commit/424da7a971308b8f33cb558e0cc4f79df82f6bd6))

### Features

- Add per-endpoint API docs fetcher replacing monolithic spec
  ([`98bbc93`](https://github.com/ebragas/recruitcrm-mcp/commit/98bbc93330ed207ed405bebf0ca75a2ed303ee43))

Replace the bash script that downloaded an 850KB monolithic OpenAPI spec with a Python script that
  fetches individual endpoint, article, and model docs from Stoplight into organized files under
  docs/recruitcrm/.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Refactoring

- **scripts**: Address PR review on fetch_api_docs
  ([`117e6ad`](https://github.com/ebragas/recruitcrm-mcp/commit/117e6adbe08bddb8e337638d86665e31943d9b5c))

- Add empty-string fallback in slugify - Filter failed items from _index.json instead of leaving
  empty paths - Remove unused endpoint_filename function - Replace unreachable return with
  RuntimeError

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>


## v0.5.1 (2026-02-26)

### Bug Fixes

- **install**: Use absolute path to uvx in Claude Desktop config
  ([`7bfa346`](https://github.com/ebragas/recruitcrm-mcp/commit/7bfa34645134d8920fe6a1c43d7591eafa30f96d))

Claude Desktop doesn't inherit the user's shell PATH, so a bare "uvx" command fails. Resolve the
  absolute path via shutil.which() during installation and write that to the config instead.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Chores

- **release**: 0.5.1
  ([`704ac59`](https://github.com/ebragas/recruitcrm-mcp/commit/704ac59143f09b83e57cd4280f4c4e404fff911e))


## v0.5.0 (2026-02-26)

### Chores

- **release**: 0.5.0
  ([`8d68ace`](https://github.com/ebragas/recruitcrm-mcp/commit/8d68ace1d6bd154da5ff9d86b821da11abea942e))

### Features

- Add curl | bash bootstrap installer and remove chmod on config
  ([#7](https://github.com/ebragas/recruitcrm-mcp/pull/7),
  [`84a8b4a`](https://github.com/ebragas/recruitcrm-mcp/commit/84a8b4a97aba5da5e82b02283cd3c8b6e20ba98d))

* fix(install): remove chmod 0o600 on Claude Desktop config file

The installer was setting restrictive permissions on claude_desktop_config.json after writing it.
  This is an opinionated change that could conflict with Claude Desktop's own expectations for its
  config file. The file already lives in the user's Application Support directory which is
  user-scoped on macOS.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* feat(install): add curl | bash bootstrap script

Adds install.sh that installs uv if missing, sources the env file so uvx is available immediately
  (no terminal restart), then hands off to the interactive Python installer via uvx.

One-liner for end users: curl -LsSf
  https://raw.githubusercontent.com/ebragas/recruitcrm-mcp/main/install.sh | bash

* fix(install): add curl preflight check and download-then-run option

- Add curl availability check at the top of install.sh with clear error - Add download-then-review
  alternative in README for security-conscious users

* fix(install): remove redundant curl preflight check

curl is the delivery mechanism for the script itself, so checking for it inside the script is
  unnecessary.

---------

Co-authored-by: Eric Bragas <eric@ebragas.com>

Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>


## v0.4.0 (2026-02-26)

### Bug Fixes

- **client**: Cap Retry-After at 120s, move imports to module level
  ([`ae298a3`](https://github.com/ebragas/recruitcrm-mcp/commit/ae298a3b31f329ba5cf8cca2979087605008683e))

- Cap Retry-After header value at 120s to match X-RateLimit-Reset behavior - Move time import to
  module level in client.py - Move time and logging imports to module level in test_client.py - Add
  tests for Retry-After cap and X-RateLimit-Reset in the past

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Chores

- **release**: 0.4.0
  ([`2694cff`](https://github.com/ebragas/recruitcrm-mcp/commit/2694cff6801d6b2a49077ec129ff33349b0d67ec))

### Features

- **client**: Add rate limit handling with retry on 429
  ([`97ba5af`](https://github.com/ebragas/recruitcrm-mcp/commit/97ba5afd8a30f8ed518b2e5e314fff1db2296312))

Catch 429 responses in client.get(), parse Retry-After / X-RateLimit-Reset headers for wait
  duration, log a warning, and retry once. If the second attempt also fails, the error is raised to
  the caller.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>


## v0.3.0 (2026-02-26)

### Bug Fixes

- Simplify uv install guidance for non-technical users
  ([`b7a6e17`](https://github.com/ebragas/recruitcrm-mcp/commit/b7a6e173b746a66b8cfcfd7d07b3ccac99e48bf1))

Drop Homebrew reference (target users won't have it) and default the auto-install prompt to Yes so
  users can just press Enter.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

- **install**: Harden installer and boost test coverage to 92%
  ([`c89f8db`](https://github.com/ebragas/recruitcrm-mcp/commit/c89f8db566b9b2e06e264b4ccde76f560fbc941c))

- Fix PATH detection after uv auto-install (advise restart instead of failing) - Add graceful
  handling for invalid JSON in existing config - Add explicit UTF-8 encoding for file I/O (Windows
  portability) - Set restrictive file permissions (0600) on config containing API key - Wrap main()
  in KeyboardInterrupt handler for clean Ctrl+C exit - Guard __main__.py with if __name__ ==
  "__main__" - Add tests for prompt_install_uv, _auto_install_uv, main() flow, and invalid JSON —
  coverage 47% → 92%

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Chores

- **release**: 0.3.0
  ([`5160e07`](https://github.com/ebragas/recruitcrm-mcp/commit/5160e075b1787becd09f19ed114e08e6636d2649))

### Continuous Integration

- Add conventional commit message validation hook
  ([`8e36b6c`](https://github.com/ebragas/recruitcrm-mcp/commit/8e36b6c96fdeb79abf64e6473778bf3a1f7962e1))

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Features

- Add one-click installer for Claude Desktop configuration
  ([`fa92dbf`](https://github.com/ebragas/recruitcrm-mcp/commit/fa92dbf6ba7d48e95578480c8356d4de9a969442))

Interactive CLI wizard that prompts for the Recruit CRM API key, detects OS, locates
  claude_desktop_config.json, backs up existing config, and injects the MCP server entry. Runnable
  via `uvx --from recruit-crm-mcp recruit-crm-mcp-install` or `python -m recruit_crm_mcp`.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>


## v0.2.0 (2026-02-25)

### Bug Fixes

- Run uv build in workflow instead of semantic-release container
  ([`965326f`](https://github.com/ebragas/recruitcrm-mcp/commit/965326fc5a7bd8dd3248288a5b050428180187dc))

The semantic-release Docker container doesn't have uv installed, so build_command = "uv build"
  fails. Disable building inside the action and run uv build as a separate workflow step where uv is
  available.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Chores

- **release**: 0.2.0
  ([`b9f0cab`](https://github.com/ebragas/recruitcrm-mcp/commit/b9f0cab82adf6c08099efedf46b5e5d8f1d87889))

### Features

- Add semantic versioning with auto-publish on merge to main
  ([`97676ba`](https://github.com/ebragas/recruitcrm-mcp/commit/97676ba766e548250e1b5ceaaab3c2ca864359ca))

Replace tag-based publish workflow with python-semantic-release. Version bumps are now driven by
  conventional commits — fix: for patch, feat: for minor, BREAKING CHANGE for major. On merge to
  main, the workflow analyzes commits, bumps pyproject.toml, creates a GitHub Release, and publishes
  to PyPI automatically.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>


## v0.1.0 (2026-02-25)
