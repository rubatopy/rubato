.PHONY: all

all:
	@make test
	@make lint

test:
	@pytest --cov=rubato --cov-report term-missing rubato/tests

test-no-rub:
	@pytest -m "not rub" --cov=rubato --cov-report term-missing rubato/tests

test-no-sdl:
	@pytest -m "not sdl" --cov=rubato --cov-report term-missing rubato/tests

lint:
	@echo "Linting Code"
	@pylint rubato

docs-live:
	@(cd docs && make live)
