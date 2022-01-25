# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = ./build
LIVEBUILDDIR  = ./build/_html
ver		      = dev

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

html:
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

bump:
	@read -p "What version should the current latest go to?" oldver
	@if [ -d latest ]; then \
		mv latest/ versions/$(oldver); \
	fi
	@make save ver=latest
	@make save

save:
	@make html
	@if [ "$(ver)" = "latest" ]; then \
		rm -rf latest; \
		cp -r ./build/html/ ./latest/; \
	else \
		rm -rf ./versions/$(ver); \
		cp -r ./build/html/ ./versions/$(ver); \
	fi
	@echo "Saved version $(ver)"

remove:
	@if [ "$(ver)" = "latest" ]; then \
		rm -rf latest; \
	else \
		rm -rf ./versions/$(ver); \
	fi
	@echo "Removed version $(ver)"

livehtml:
	@sphinx-autobuild "$(SOURCEDIR)" "$(LIVEBUILDDIR)" $(SPHINXOPTS) $(O) --watch ./source
