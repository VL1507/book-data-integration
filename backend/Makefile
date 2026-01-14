# app
runapp:
	uv run src/__main__.py

format:
	uv run ruff format
	uv run ruff check --fix

lint:
	uv run ruff check
	uv run mypy .

format_check:
	uv run ruff check

test:
	uv run pytest

type_check:
	uv run mypy . --explicit-package-bases

precommit:
	make format_check
	make test
	make type_check


migrate-create:
	alembic revision --autogenerate -m ${MES}

migrate-apply:
	alembic upgrade head