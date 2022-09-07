#!/bin/bash
# A script to run various automation on rubato


help_text() {
    if [ $# -ne 0 ]
    then
        echo "Unknown argument: '$1'"
    else
        echo "Usage: $0 [options]"
    fi
}

delete() {
    case $1 in
        bin|b)
            cd rubato
            find . -name "*.pyd" -type f -delete
            find . -name "*.so" -type f -delete
            cd ..
            ;;
        c)
            cd rubato
            find . -name "*.cpp" -not -name "cdraw.cpp" -type f -delete
            find . -name "*.c" -type f -delete
            cd ..
            ;;
        *)
            rm -rf build
            delete bin
            delete c
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
    -h|--help)
        help_text
        ;;
    build|b)
        build $2
        ;;
    demo|demos|dem)
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
        pip install --editable .[dev]
        pip install --editable .[docs]
        build f
        ;;
    precommit|pc|pre|p)
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
    publish-wheel|publish|pub)
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
