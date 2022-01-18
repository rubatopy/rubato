from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Rubato is a Python game engine that builds off of PyGame to make a cleaner and more efficient game engine."
LONG_DESCRIPTION = open("README.md").read() + "\n\n" + open("CHANGELOG.md").read()

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
    install_requires=["pygame==2.0.2", "typeguard==2.13.0"],
    python_requires=">=3.10",
)
