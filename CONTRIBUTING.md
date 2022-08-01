# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Setting up dev environment

Setting up your environment is easy. Just run:

```shell
make setup
```

This will take a couple minutes the first time so be patient. Once this finishes, everything is ready to go!

rubato is a Cython project. To compile the code, run:

```shell
make build
```

### To run tests

From the repository root, run:

```shell
make test
```

This will run all the tests. There are also more make targets for specific tests.

```shell
make all # Run all tests and linting
make # same as make all
make test # Run all tests
make lint # Run linting
make test-no-sdl # Run tests that don't need SDL
make test-no-rub # Run tests that don't need Rubato initialized
make test-rub # Run tests that need Rubato initialized
make test-sdl # Run tests that need SDL
make test-indiv # Run individual tests. Must specify test parameter. (e.g. make test-indiv test=test_foo)
```

## Suggest Improvements

Open up issues:

https://github.com/rubatopy/rubato/issues

## Pull Request Process

1. Make to remove any unnecessary print statements and remove all `TODO` comments.
2. Update the `CHANGELOG.md` with details of changes.
3. Make sure that all changes have unit-tests.
4. Make sure that all Github Actions pass.
5. The pull request will then be review and merged by a maintainer.

## Documentaion

The docs are built and publish automatically

### To run the docs locally

```shell
pip install -e .[docs] # install requirements for docs
make docs-live # start doc server
```

### Docstring Guide

This project uses a modified version of the Google Docstring Format.

Every function, property, and attribute should have type annotations for its arguments and return type (None return types
are assumed and are therefore not needed). However, all **public** functions, properties and attributes should be documented.
Docstrings should start with a short summary of the function, property or attribute, followed by any notes or warnings.
Then any arguments and return types should be documented (types do not need to be specified). For classes, any attributes (NOT property methods)
should also be documented with types. Finally, any examples should be included at the end. Correct spelling, syntax, and punctuation is required.
This means capitalizing the first letter of sentences and always adding periods to the end of sentences.

Docstrings that need extra formatting (e.g. code blocks, references to other functions, etc.) should be formatted using Sphinx RST.

Here is an example class which includes attributes, methods, and properties:

```python
class Foo:
    """
    Foo is a class that does bar.

    Warning:
        The Foo class is depricated.

    Args:
        bar: The bar argument.
        baz: The baz argument.

    Attributes:
        bar (int): The bar attribute.
        baz (str): The baz attribute.
    """
    def __init__(self, bar, baz):
        self.bar = bar
        self.baz = baz

    @property
    def foo(self) -> float:
        """The foo property."""
        return 0.1

    @foo.setter
    def foo(self, value: float):
        # setters do not need docstrings
        pass

    def foobar(self, bar: int, baz: str) -> str:
        """
        The foobar method.

        Args:
            bar: The bar argument.
            baz: The baz argument.

        Returns:
            The merged bar and baz arguments.

        Example:
            >>> foo = Foo(1, 'a')
            >>> foo.foobar(2, 'b')
            '2b'
        """
        return bar + baz
```

Feel free to look at the source code for more examples.

### RST Header Conventions

The following conventions are used for RST headers.

```rst
##
H1
##

**
H2
**

H3
==

H4
--

H5
__

H6
```

## Releasing new versions

1.  Update`Changelod.md` so that unreleased becomes this version and update the link at the bottom of the file.
    (following the format as the other links). Also remove unused sections in the unreleased section.

2.  Push the changelog to Github and release a new Github release. Make sure to end the release description with:

    ```markdown
    As always, see the [`CHANGELOG.md`](https://github.com/rubatopy/rubato/blob/{VERSION_NAME}/CHANGELOG.md) and the [documentation](https://rubato.app/{VERSION_NAME}) for more details.
    ```

3.  Once the automatic release is complete, build and upload the apple silicon build with on a apple silicon Mac:

    ```shell
    RUBATO_VERSION={VERSION_NAME} make pypi-publish-wheels
    ```

    Also upload the wheel to the github release.

4.  Finally, add the following to the top of the changelog and push:

    ```markdown
    ## [Unreleased]

    ### Breaking Changes

    ### Added

    ### Changed

    ### Removed

    ### Fixed
    ```
