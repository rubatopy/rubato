# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Suggest Improvements

Open up issues:

https://github.com/rubatopy/rubato/issues

## Pull Request Process

1. Make to remove any unnecessary print statements and remove all `TODO` comments.
2. Update the `CHANGELOG.md` with details of changes.
3. The pull request will be merged by the maintainer.

## Documentaion

The docs are built and publish automatically

### To run the docs locally

```bash
pip install --editable .[docs] # install requirements for docs
(cd docs && make live) # start doc server
```

### RST Header Conventions

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
