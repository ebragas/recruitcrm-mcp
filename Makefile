.PHONY: venv clean test lint check

venv:
	uv sync

clean:
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

test:
	uv run pytest

lint:
	uv run ruff check src/ tests/

check: lint test
