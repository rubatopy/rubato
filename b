#!/bin/bash
# A script to run various automation on rubato


help_text() {
    tab="    "
    if [[ $# -ne 0 ]]
    then
        echo "Unknown arguments: '$@'"
        echo "Try './b --help' for more information."
    else
        echo "Usage: ./b [command] [flags]"
        echo ""
        echo "Options:"
        echo "${tab}help, --help, -h: Show this help manual (default)"
        echo "${tab}build, b: Cythonize and build rubato"
        echo "${tab}${tab}--force, -f: Force rubato to rebuild"
        echo "${tab}demo, dem: Run the demos in quick succession"
        echo "${tab}delete, del:"
        echo "${tab}${tab}--all, -a: Delete all rubato build files (default)"
        echo "${tab}${tab}--dir, -d: Delete only the build directory"
        echo "${tab}${tab}--bin, -b: Delete only the binary files"
        echo "${tab}${tab}--cython, -c: Delete only the C/C++ files"
        echo "${tab}docs, doc:"
        echo "${tab}${tab}--save, -s: Build and save the documentation (default)"
        echo "${tab}${tab}--live, -l: Start a local server hosting the documentation"
        echo "${tab}${tab}--clear, -c: Clear the documentation build directory"
        echo "${tab}lint, l: Run linting on rubato"
        echo "${tab}test, t:"
        echo "${tab}${tab}--test, -t: Run the rubato test suite (default)"
        echo "${tab}${tab}--build, -b: Build rubato for testing without running tests"
        echo "${tab}${tab}--quick, -q: Run the tests without forcing a rebuild"
        echo "${tab}${tab}--no-build, -n: Run the tests without building"
        echo "${tab}setup, s: Install all needed dependencies for developing rubato"
        echo "${tab}precommit, pre: Run the precommit script (run every common test)"
        echo "${tab}pypi: Build the project for pypi"
        echo "${tab}publish-wheel, publish: Build and publish the wheel to pypi"
    fi
}

delete() {
    case $1 in
        --bin|-b)
            echo "Deleting binary files..."
            find . -name "*.pyd" -type f -delete
            find . -name "*.so" -type f -delete
            ;;
        --cython|-c)
            echo "Deleting cython files..."
            find . -name "*.cpp" -not -name "cdraw.cpp" -type f -delete
            find . -name "*.c" -type f -delete
            ;;
        --dir|-d)
            echo "Deleting build directory..."
            rm -rf build
            ;;
        *|--all|-a)
            delete --dir --bin --cython
            ;;
    esac
    shift
    if [[ $# -gt 0 ]]
    then
        delete "$@"
    fi
}

build() {
    case $1 in
        --force|-f)
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
    case $1 in
        --clear|-c)
            cd docs
            rm -rf build
            cd ..
            ;;
        --live|-l)
            ./b del -b
            ./b doc -c
            cd docs
            sphinx-autobuild "$SOURCEDIR" "$BUILDDIR" -b $BUILDER $O --watch ../rubato
            cd ..
            if [[ -d build ]]
            then
                echo "Restoring binary files..."
                ./b b >/dev/null
            fi
            ;;
        *|--save|-s)
            ./b del -b
            ./b doc -c
            cd docs
            python -m $SPHINXBUILD -W --keep-going -T -b $BUILDER "$SOURCEDIR" "$BUILDDIR"
            touch build/html/_modules/robots.txt
            cd ..
            if [[ -d build ]]
            then
                echo "Restoring binary files..."
                ./b b >/dev/null
            fi
            ;;
    esac
    shift
    if [[ $# -gt 0 ]]
    then
        doc "$@"
    fi
}

tests() {
    case $1 in
        --build|-b)
            delete
            CFLAGS=-DCYTHON_TRACE=1 TEST_MODE=1 python setup.py build_ext --inplace --define CYTHON_TRACE
            ;;
        --quick|-q)
            TEST_MODE=1 python setup.py build_ext --inplace --define CYTHON_TRACE
            tests t
            ;;
        --no-build|-n)
            pytest --cov=rubato tests
            ;;
        *|--test|-t)
            tests -b -n
            ;;
    esac
    shift
    if [[ $# -gt 0 ]]
    then
        tests "$@"
    fi
}

ogdir="$( pwd )"
cd "$( dirname -- "$0" )"
case $1 in
    help|--help|-h)
        help_text
        ;;
    build|b)
        shift
        build "$@"
        ;;
    demo|dem)
        ./b b
        cd demo
        ./_run_all.sh
        ;;
    delete|del)
        shift
        delete "$@"
        ;;
    docs|doc)
        shift
        doc "$@"
        ;;
    lint|l)
        ./b del -b
        echo "Linting Code..."
        pylint rubato
        if [[ -d build ]]
        then
            echo "Restoring binary files..."
            ./b b >/dev/null
        fi
        ;;
    test|t)
        shift
        tests "$@"
        ;;
    setup|s)
        git submodule update --init --recursive
        pip install --editable .[dev,docs]
        build f
        ;;
    precommit|pre)
        ./b del
        ./b doc
        ./b l
        echo "Building rubato..."
        ./b t -b >/dev/null
        ./b t -n
        cd demo
        ./_run_all.sh
        cd ..
        ;;
    pypi)
        rm -rf dist
        python -m build
        ;;
    publish-wheel|publish)
        rm -rf dist
        python -m build
        python -m twine upload dist/*.whl
        ;;
    *)
        help_text "$@"
        ;;
esac
cd "$ogdir"
