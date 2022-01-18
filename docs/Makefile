# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = .

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

html: Makefile
	@mkdir ./temp
	@mv ./source ./temp && mv ./doctrees ./temp && mv make.bat ./temp && mv Makefile ./temp && mv .nojekyll ./temp
	@find ! -regex '^./temp\(/.*\)?' ! -regex '.' -delete
	@mv ./temp/source . && mv ./temp/doctrees . && mv ./temp/make.bat . && mv ./temp/Makefile . && mv ./temp/.nojekyll .
	@rmdir ./temp
	@rm -rf ./source/generated
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@mv -v ./html/* . && rm -rf ./html

