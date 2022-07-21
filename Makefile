.PHONY: all

all:
	@make test
	@make lint
	@make demos

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

demos:
	@cd demo && ./_run_all.sh

SPHINXBUILD   ?= sphinx
SOURCEDIR     = source
BUILDDIR      = ./build/html
LIVEBUILDDIR  = ./build/_html
BUILDER          = dirhtml

docs-save:
	@make docs-clear
	@cd docs && python -m $(SPHINXBUILD) -W --keep-going -T -q -b $(BUILDER) "$(SOURCEDIR)" "$(BUILDDIR)"
	@cd docs && touch build/html/_modules/robots.txt

docs-test:
	@make docs-clear
	@cd docs && python -m $(SPHINXBUILD) -b $(BUILDER) "$(SOURCEDIR)" "$(LIVEBUILDDIR)"

docs-live:
	@make docs-clear
	@cd docs && sphinx-autobuild "$(SOURCEDIR)" "$(LIVEBUILDDIR)" -b $(BUILDER) $(O) --watch ../rubato

docs-clear:
	@cd docs && rm -rf build
