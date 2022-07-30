.PHONY: all build

all:
	@make test
	@make lint

test:
	@pytest --cov=rubato --cov-report term-missing tests -s

test-rub:
	@pytest -m "rub" --cov=rubato --cov-report term-missing tests -s

test-sdl:
	@pytest -m "sdl or rub" --cov=rubato --cov-report term-missing tests -s

test-no-rub:
	@pytest -m "not rub" --cov=rubato --cov-report term-missing tests

test-no-sdl:
	@pytest -m "not sdl and not rub" --cov=rubato --cov-report term-missing tests -s

test-indiv:
	@pytest tests -k "$(test)"

lint:
	@echo "Linting Code"
	@pylint rubato

docs-live:
	@(cd docs && make live)

build:
	@python setup.py build_ext --inplace
