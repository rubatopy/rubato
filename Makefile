.PHONY: all

all:
	@make test
	@make lint

test:
	@pytest --cov=rubato --cov-report term-missing rubato/tests

lint:
	@echo "Linting Code"
	@pylint rubato
