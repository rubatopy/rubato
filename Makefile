.PHONY: all build

all: test lint

test: build
	@pytest --cov=rubato --cov-report term-missing tests -s

test-rub: build
	@pytest -m "rub" --cov=rubato --cov-report term-missing tests -s

test-sdl: build
	@pytest -m "sdl or rub" --cov=rubato --cov-report term-missing tests -s

test-no-rub: build
	@pytest -m "not rub" --cov=rubato --cov-report term-missing tests

test-no-sdl: build
	@pytest -m "not sdl and not rub" --cov=rubato --cov-report term-missing tests -s

test-indiv: build
	@pytest tests -k "$(test)"

lint:
	@echo "Linting Code"
	@pylint rubato

docs-live:
	@(cd docs && make live)

build:
	@python setup.py build_ext --inplace

setup:
	@git submodule update --init --recursive
	@pip install --editable .[dev]
	@pre-commit install -f
	@pre-commit run --all-files
	@python setup.py build_ext --inplace

delete-bin:
	@cd rubato && find . -name "*.pyd" -type f -delete
	@cd rubato && find . -name "*.so" -type f -delete
	@rm -rf build

delete-c:
	@cd rubato && find . -name "*.c" -type f -delete
	@rm -rf build

delete-build: delete-bin delete-c

pypi-build:
	@rm -rf dist
	@python -m build
