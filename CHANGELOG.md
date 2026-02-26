# CHANGELOG


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
