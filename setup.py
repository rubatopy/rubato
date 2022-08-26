# pylint: disable=all
from setuptools import setup, find_packages

VERSION = "0.1.0"
DESCRIPTION = "A lightweight, developer-first game engine built for Python."
LONG_DESCRIPTION = (open("README.md").read() + "\n\n" +
                    open("CHANGELOG.md").read())

setup(
    name="rubato",
    version=VERSION,
    author="Martin Chaperot, Yamm Elnekave, Tomer Sedan",
    author_email="m.artin.chapino@gmail.com",
    license="MIT",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/tinmarr/rubato",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().split("\n"),
    python_requires=">=3.10",
)
