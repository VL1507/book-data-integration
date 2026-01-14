runapp:
	uv run scrapy crawl ${spider}

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
