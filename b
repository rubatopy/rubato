#!/bin/bash
# A script to run various automation on rubato


help_text() {
    tab="    "
    if [ $# -ne 0 ]
    then
        echo "Unknown argument: '$1'"
    else
        echo "Usage: ./b [options]"
        echo ""
        echo "Options:"
        echo "${tab}--help, -h: Show this help text"
        echo "${tab}build, b: Build the project"
        echo "${tab}${tab}force: Force a rebuild"
        echo "${tab}demo, dem: Run the demos"
        echo "${tab}delete, del: Delete the build directory"
        echo "${tab}${tab}bin, b: Delete the binary files"
        echo "${tab}${tab}c: Delete the c files"
        echo "${tab}docs, doc: Start a live server of the documentation"
        echo "${tab}${tab}clear, c: Clear the documentation build directory"
        echo "${tab}${tab}save, s: Save the documentation build directory"
        echo "${tab}lint, l: Run the linter"
        echo "${tab}test, t: Run the testing flow"
        echo "${tab}${tab}build, b: Build the project for testing"
        echo "${tab}${tab}quick, q: Run the tests without force rebuilding"
        echo "${tab}${tab}test, t: Run the tests without building"
        echo "${tab}setup, s: Setup the project"
        echo "${tab}precommit, pre: Run the precommit script"
        echo "${tab}pypi: Build the project for pypi"
        echo "${tab}publish-wheel, publish: Build and publish the wheel to pypi"
    fi
}

delete() {
    case $1 in
        bin|b)
            echo "Deleting binary files..."
            find . -name "*.pyd" -type f -delete
            find . -name "*.so" -type f -delete
            ;;
        c)
            echo "Deleting c files..."
            find . -name "*.cpp" -not -name "cdraw.cpp" -type f -delete
            find . -name "*.c" -type f -delete
            ;;
        *)
            echo "Deleting build directory..."
            rm -rf build
            delete bin
            delete c
            ;;
    esac
}

build() {
    case $1 in
        force|f)
            delete
            build
            ;;
        *)
            python setup.py build_ext --inplace
            ;;
    esac
}

doc() {
    SPHINXBUILD="sphinx"
    SOURCEDIR="source"
    BUILDDIR="./build/html"
    BUILDER="dirhtml"
    endmsg="\033[0;34mBuild was deleted. Make sure to rebuild. \033[0m"
    case $1 in
        clear|c)
            cd docs
            rm -rf build
            cd ..
            ;;
        save|s)
            ./b del b
            ./b doc c
            cd docs
            python -m $SPHINXBUILD -W --keep-going -T -b $BUILDER "$SOURCEDIR" "$BUILDDIR"
            touch build/html/_modules/robots.txt
            cd ..
            echo -e $endmsg
            ;;
        *)
            ./b del b
            ./b doc c
            cd docs
            sphinx-autobuild "$SOURCEDIR" "$BUILDDIR" -b $BUILDER $O --watch ../rubato
            cd ..
            echo -e $endmsg
            ;;
    esac
}

tests() {
    case $1 in
        build|b)
            CFLAGS=-DCYTHON_TRACE=1 TEST_MODE=1 python setup.py build_ext --force --inplace --define CYTHON_TRACE
            ;;
        quick|q)
            TEST_MODE=1 python setup.py build_ext --inplace --define CYTHON_TRACE
            tests t
            ;;
        test|t)
            pytest --cov=rubato tests
            ;;
        *)
            tests b
            tests t
            ;;
    esac
}

ogdir="$( pwd )"
cd "$( dirname -- "$0" )"
case $1 in
    --help|-h)
        help_text
        ;;
    build|b)
        build $2
        ;;
    demo|dem)
        ./b b
        cd demos
        ./_run_all.sh
        ;;
    delete|del)
        delete $2
        ;;
    docs|doc)
        doc $2
        ;;
    lint|l)
        ./b del b
        echo "Linting Code..."
        pylint rubato
        if [ -d build ]
        then
            ./b b >/dev/null
        fi
        ;;
    test|t)
        tests $2
        ;;
    setup|s)
        git submodule update --init --recursive
        pip install --editable .[dev,docs]
        build f
        ;;
    precommit|pre)
        ./b doc s
        ./b lint
        echo "Building rubato..."
        ./b t b >/dev/null
        ./b t t
        cd demos
        ./_run_all.sh
        cd ..
        ;;
    pypi)
        rm -rf dist
        python -m build
        ;;
    publish-wheel|publish)
        rm -rf dist
        pip install twine
        python -m build
        python -m twine upload dist/*.whl
        ;;
    *)
        help_text $1
        ;;
esac
cd "$ogdir"
