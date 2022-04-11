@REM Auto generated file
@echo off

SET SOURCEDIR=source
SET BUILDDIR=.
SET LIVEBUILDDIR=.\build\_html
SET BUILDER		=dirhtml

IF /I "%1"=="save" GOTO save
IF /I "%1"=="test" GOTO test
IF /I "%1"=="live" GOTO live
IF /I "%1"=="clear" GOTO clear
GOTO error

:save
	@%SPHINXBUILD% "%SOURCEDIR%" "%BUILDDIR%"
	GOTO :EOF

:test
	@make clear
	@%SPHINXBUILD% -b %BUILDER% "%SOURCEDIR%" "%LIVEBUILDDIR%"
	GOTO :EOF

:live
	@make clear
	@sphinx-autobuild "%SOURCEDIR%" "%LIVEBUILDDIR%" -b %BUILDER% %O% --watch ../rubato
	GOTO :EOF

:clear
	@rm -rf build
	GOTO :EOF

:error
    IF "%1"=="" (
        ECHO make: *** No targets specified and no makefile found.  Stop.
    ) ELSE (
        ECHO make: *** No rule to make target '%1%'. Stop.
    )
    GOTO :EOF
