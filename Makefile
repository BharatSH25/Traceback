.PHONY: dev test lint fmt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	python -m ruff check .

fmt:
	python -m ruff format .
