# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = ./build
LIVEBUILDDIR  = ./build/_html

.PHONY: save

save:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -t $(ver)
	@rm -rf $(ver)
	@cp -r ./build/html/ ./$(ver)/
	@echo "Saved $(ver) version"

live:
	@sphinx-autobuild "$(SOURCEDIR)" "$(LIVEBUILDDIR)" $(SPHINXOPTS) $(O) --watch ../rubato

clear:
	@rm -rf build

html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -t dev
	@rm -rf dev
	@cp -r ./build/html/ ./dev/