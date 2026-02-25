.PHONY: venv clean test integration-test lint check

venv:
	uv sync

clean:
	rm -rf .venv
	find . -type d -name '__pycache__' -prune -exec rm -rf '{}' +
	find . -type d -name '*.egg-info' -prune -exec rm -rf '{}' +
	find . -type f -name '*.pyc' -delete

test:
	uv run pytest -m "not integration"

integration-test:
	uv run pytest -m integration --tb=short

lint:
	uv run ruff check src/ tests/

check: lint test
