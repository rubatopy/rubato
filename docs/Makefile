# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXBUILD   ?= sphinx-multiversion
SOURCEDIR     = source
BUILDDIR      = .
LIVEBUILDDIR  = ./build/_html

.PHONY: save

save:
	@$(SPHINXBUILD) "$(SOURCEDIR)" "$(BUILDDIR)"

test:
	@make clear
	@$(SPHINXBUILD) "$(SOURCEDIR)" "$(LIVEBUILDDIR)"

live:
	@make clear
	@sphinx-autobuild "$(SOURCEDIR)" "$(LIVEBUILDDIR)" $(SPHINXOPTS) $(O) --watch ../rubato

clear:
	@rm -rf build
