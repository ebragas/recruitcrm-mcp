.PHONY: setup venv clean test coverage integration-test integration-sweep mcp-test mcp-live-test smoke lint check fetch-docs

setup: venv
	git config core.hooksPath .githooks

venv:
	uv sync

clean:
	rm -rf .venv
	find . -type d -name '__pycache__' -prune -exec rm -rf '{}' +
	find . -type d -name '*.egg-info' -prune -exec rm -rf '{}' +
	find . -type f -name '*.pyc' -delete

test:
	uv run pytest -m "not integration and not mcp_live"

coverage:
	uv run pytest -m "not integration and not mcp_live" --cov=recruit_crm_mcp --cov-report=term-missing --cov-report=xml:coverage.xml

integration-test:
	uv run pytest -m integration --tb=short

integration-sweep:
	uv run python -m tests.integration._sweep

mcp-test:
	uv run pytest tests/mcp -m "not mcp_live"

mcp-live-test:
	uv run pytest tests/mcp -m mcp_live --tb=short

smoke:
	uv run scripts/smoke.py

lint:
	uv run ruff check src/ tests/

check: lint test

fetch-docs:
	python3 scripts/fetch_api_docs.py
