from setuptools import setup, find_packages

VERSION = "0.0.0"
DESCRIPTION = "This is a Pygame Game Engine"
LONG_DESCRIPTION = open("README.md").read() + "\n\n" + open("CHANGELOG.md").read()

setup(
    name="PygamePlus",
    version=VERSION,
    author="Martin Chaperot, Yamm Elnekave, Tomer Sedan",
    author_email="test@test.com",
    license="MIT",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pygame"],
    python_requires=">=3.9",
    include_package_data=True,
)
