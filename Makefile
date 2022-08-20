.PHONY: all build


all: test lint demos

build-test: delete-build
	@export CFLAGS=-DCYTHON_TRACE=1
	@export TEST_MODE=1 && python setup.py build_ext --force --inplace --define CYTHON_TRACE

test: build-test
	@pytest --cov=rubato --cov-report term-missing --log-format="%(asctime)s %(levelname)s %(thread)d %(message)s" tests 

test-rub: build-test
	@pytest -m "rub" --cov=rubato --cov-report term-missing tests -s

test-sdl: build-test
	@pytest -m "sdl or rub" --cov=rubato --cov-report term-missing tests -s

test-no-rub: build-test
	@pytest -m "not rub" --cov=rubato --cov-report term-missing tests

test-no-sdl: build-test
	@pytest -m "not sdl and not rub" --cov=rubato --cov-report term-missing tests -s

test-indiv: build-test
	@pytest tests -k "$(test)"

lint: delete-bin
	@echo "Linting Code"
	@-pylint rubato 
	@-[ -d build ] && make build

demos: build
	@cd demo && ./_run_all.sh

SPHINXBUILD   ?= sphinx
SOURCEDIR     = source
BUILDDIR      = ./build/html
LIVEBUILDDIR  = ./build/_html
BUILDER          = dirhtml

docs-save: docs-clear delete-build
	@cd docs && python -m $(SPHINXBUILD) -W --keep-going -T -q -b $(BUILDER) "$(SOURCEDIR)" "$(BUILDDIR)"
	@cd docs && touch build/html/_modules/robots.txt

docs-test: docs-clear delete-build
	@cd docs && python -m $(SPHINXBUILD) -b $(BUILDER) "$(SOURCEDIR)" "$(LIVEBUILDDIR)"

docs-live: docs-clear delete-bin
	@bash -c "trap 'make build;echo -e \"\033[0;34mctrl+c to exit \033[0m\"' SIGINT; (cd docs && sphinx-autobuild "$(SOURCEDIR)" "$(LIVEBUILDDIR)" -b $(BUILDER) $(O) --watch ../rubato)"

docs-clear:
	@cd docs && rm -rf build

build:
	@python setup.py build_ext --inplace

rebuild: delete-build build

watch:
	@bash ./watchBuild.sh

setup:
	@git submodule update --init --recursive
	@pip install --editable .[dev]
	@pip install --editable .[docs]
	@python setup.py build_ext --inplace

delete-bin:
	@cd rubato && find . -name "*.pyd" -type f -delete
	@cd rubato && find . -name "*.so" -type f -delete

delete-c:
	@cd rubato && find . -name "*.cpp" -not -name "cdraw.cpp" -type f -delete
	@cd rubato && find . -name "*.c" -type f -delete

delete-build: delete-bin delete-c
	@rm -rf build

pypi-build:
	@rm -rf dist
	@python -m build

pypi-publish-wheels:
	@rm -rf dist
	@pip install build twine
	@python -m build
	@python -m twine upload dist/*.whl
