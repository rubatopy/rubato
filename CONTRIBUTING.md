# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Setting up dev environment

-   **Linux:** The GNU C Compiler (gcc) is usually present, or easily available through the package system. On Ubuntu or Debian, for instance, it is part of the `build-essential` package. Next to a C compiler, Cython requires the Python header files. On Ubuntu or Debian, the command `sudo apt-get install build-essential python3-dev` will fetch everything you need.
-   **Mac OS X:** To clang, install the XCode CLI with `xcode-select –install`.
-   **Windows:** Get the Microsoft Build Tools [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/). You need the **MSVC** compiler, and the SDK for your Windows version. To download make using Chocolatey, go [here](https://stackoverflow.com/a/57042516).

Setting up your environment is easy. In a bash shell just run:

```shell
./b setup
```

On Windows you need to be using Git Bash or WSL.

This will take a couple minutes the first time so be patient. Once this finishes, everything is ready to go!

#### rubato is a Cython project. To compile the code, run:

```shell
./b build
```

### To run tests

To run most major tests, run the following from the repository root:

```shell
./b precommit
```

## Automation documentation

There are many more commands you can use to aid in testing, building, and releasing for rubato development.
Run `./b --help` in a bash shell for more information.

## Suggest Improvements

Open up issues:

https://github.com/rubatopy/rubato/issues

## Pull Request Process

1. Make to remove any unnecessary print statements and remove all `TODO` comments.
2. Update the `CHANGELOG.md` with details of changes.
3. Make sure that all changes have unit-tests.
4. Make sure that all GitHub Actions pass.
5. The pull request will then be review and merged by a maintainer.

## Documentaion

The docs are built and publish automatically

### To run the docs locally

```shell
pip install -e .[docs] # install requirements for docs
./b docs -l # start doc server
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
    """
    def __init__(self, bar: int, baz: str):
        self.bar: int = bar
        """The bar attribute."""
        self.baz: str = baz
        """The baz attribute."""

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

1. Choose a version name. When choosing a version name, use the following guidelines, taken from [py-pkgs.org](https://py-pkgs.org/):

    - Patch release (0.1.0 -> 0.1.1): patch releases are typically used for bug fixes, which are backward compatible. Backward compatibility refers to the compatibility of your package with previous versions of itself. For example, if a user was using v0.1.0 of your package, they should be able to upgrade to v0.1.1 and have any code they previously wrote still work. It’s fine to have so many patch releases that you need to use two digits (e.g., 0.1.27).
    - Minor release (0.1.0 -> 0.2.0): a minor release typically includes larger bug fixes or new features that are backward compatible, for example, the addition of a new function. It’s fine to have so many minor releases that you need to use two digits (e.g., 0.13.0).
    - Major release (0.1.0 -> 1.0.0): release 1.0.0 is typically used for the first stable release of your package. After that, major releases are made for changes that are not backward compatible and may affect many users. Changes that are not backward compatible are called “breaking changes”. For example, changing the name of one of the modules in your package would be a breaking change; if users upgraded to your new package, any code they’d written using the old module name would no longer work, and they would have to change it.

2. Update the version number in `setup.cfg`

3. Update `Changelod.md` so that unreleased becomes this version and update the links at the top of the file. (following the format as the other links). Also remove unused sections in the unreleased section.

4. Push the changelog to Github and release a new Github release. Make sure to end the release description with:

    ```markdown
    As always, see the [`CHANGELOG.md`](https://github.com/rubatopy/rubato/blob/{VERSION_NAME}/CHANGELOG.md) and the [documentation](https://rubato.app/{VERSION_NAME}) for more details.
    ```

5. Once the automatic release is complete, build and upload the apple silicon build with on a apple silicon Mac:

    ```shell
    ./b publish-wheels {VERSION_NAME}
    ```

    Also upload the wheel to the github release.

6. Finally, add the following to the top of the changelog and push:

    ```markdown
    ## [Unreleased] - October 30, 2022 (Expected)

    ### Breaking Changes

    ### Added

    ### Changed

    ### Removed

    ### Fixed
    ```

7. Close the relevent milestones and issues
