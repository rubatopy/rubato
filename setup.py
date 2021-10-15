from setuptools import setup, find_packages

VERSION = "0.1.0"
DESCRIPTION = "This is a Pygame Game Engine"
LONG_DESCRIPTION = open("README.md").read() + "\n\n" + open("CHANGELOG.md").read()

setup(
    name="pgp",
    version=VERSION,
    author="Martin Chaperot, Yamm Elnekave, Tomer Sedan",
    author_email="m.artin.chapino@gmail.com",
    license="MIT",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().split("\n"),
    python_requires=">=3.10",
)
