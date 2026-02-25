# CHANGELOG


## v0.2.0 (2026-02-25)

### Bug Fixes

- Run uv build in workflow instead of semantic-release container
  ([`965326f`](https://github.com/ebragas/recruitcrm-mcp/commit/965326fc5a7bd8dd3248288a5b050428180187dc))

The semantic-release Docker container doesn't have uv installed, so build_command = "uv build"
  fails. Disable building inside the action and run uv build as a separate workflow step where uv is
  available.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Features

- Add semantic versioning with auto-publish on merge to main
  ([`97676ba`](https://github.com/ebragas/recruitcrm-mcp/commit/97676ba766e548250e1b5ceaaab3c2ca864359ca))

Replace tag-based publish workflow with python-semantic-release. Version bumps are now driven by
  conventional commits — fix: for patch, feat: for minor, BREAKING CHANGE for major. On merge to
  main, the workflow analyzes commits, bumps pyproject.toml, creates a GitHub Release, and publishes
  to PyPI automatically.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>


## v0.1.0 (2026-02-25)
