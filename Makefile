.PHONY: setup venv clean test coverage integration-test lint check

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
	uv run pytest -m "not integration"

coverage:
	uv run pytest -m "not integration" --cov=recruit_crm_mcp --cov-report=term-missing --cov-report=xml:coverage.xml

integration-test:
	uv run pytest -m integration --tb=short

lint:
	uv run ruff check src/ tests/

check: lint test
