#!/bin/bash
# A script to run various automation on rubato
exit_with=0

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
        echo "${tab}test, t: Run the rubato test suite. The next argument is a search term to grep the output with."
        echo "${tab}setup, s: Install all needed dependencies for developing rubato"
        echo "${tab}precommit, pre: Run the precommit script (run every common test)"
        echo "${tab}pypi: Build the project for pypi"
        echo "${tab}publish-wheels, wheels <version_name>: Build and publish the wheel to pypi"
    fi
}

delete() {
    case $1 in
        --bin|-b)
            echo "Deleting binary files..."
            cd rubato
            find . -name "*.pyd" -type f -delete
            find . -name "*.so" -type f -delete
            exit_with="$(expr $?+$exit_with)"
            cd ..
            ;;
        --cython|-c)
            echo "Deleting cython files..."
            cd rubato
            find . -name "*.cpp" -not -name "cdraw.cpp" -type f -delete
            find . -name "*.c" -type f -delete
            exit_with="$(expr $?+$exit_with)"
            cd ..
            ;;
        --dir|-d)
            echo "Deleting build directory..."
            rm -rf build
            exit_with="$(expr $?+$exit_with)"
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
            TEST_MODE=1 python setup.py build_ext -j 6 --inplace --define CYTHON_TRACE
            exit_with="$(expr $?+$exit_with)"
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
            python -m $SPHINXBUILD -T -b $BUILDER "$SOURCEDIR" "$BUILDDIR"
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
        *)
            build
            if [ -z "$1" ]
            then
                pytest --cov=rubato tests
            else
                pytest --cov=rubato tests | grep "$1"
            fi
            exit_with="$(expr $?+$exit_with)"
            ;;
    esac
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
        exit_with="$(expr $?+$exit_with)"
        if [[ -d build ]]
        then
            echo "Restoring binary files..."
            ./b b >/dev/null
            exit_with="$(expr $?+$exit_with)"
        fi
        ;;
    test|t)
        shift
        tests "$@"
        ;;
    setup|s)
        pip install Cython==3.0.0a11
        python setup.py egg_info
        pip install `grep -v '^\[' *.egg-info/requires.txt`
        exit_with="$(expr $?+$exit_with)"
        build -f
        exit_with="$(expr $?+$exit_with)"
        pip install -e .
        exit_with="$(expr $?+$exit_with)"
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
        delete
        rm -rf dist
        python -m build
        exit_with="$(expr $?+$exit_with)"
        ;;
    publish-wheels|wheels)
        shift
        if [[ $# -eq 0 ]]
        then
            echo "No version specified"
            exit 1
        fi
        rm -rf dist
        read -p "Confirm version $1? [y/N]: " -r response
        if [[ $response =~ ^[Yy]$ ]]
        then
            BRANCH="$(git branch --show-current)"
            git checkout "$1"
            delete
            echo "Building wheels..."
            python -m build
            echo "Uploading wheels..."
            python -m twine upload dist/*.whl
            git checkout "$BRANCH"
        else
            echo "Aborting..."
        fi
        ;;
    *)
        help_text "$@"
        ;;
esac
cd "$ogdir"

if [[ $exit_with -ne 0 ]]
then
    exit 1
else
    exit 0
fi
