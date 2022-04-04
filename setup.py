# pylint: disable=all
from setuptools import setup, find_packages

VERSION = "1.2.0"
DESCRIPTION = "A lightweight, developer-first game engine built for Python."
LONG_DESCRIPTION = (open("README.md").read() + "\n\n" + open("CHANGELOG.md").read())

setup(
    name="rubato",
    version=VERSION,
    author="Martin Chaperot, Yamm Elnekave, Tomer Sedan",
    author_email="m.artin.chapino@gmail.com",
    license="MIT",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/rubatopy/rubato",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().split("\n")[5:],
    python_requires=">=3.10",
    package_data={"rubato": ["static/fonts/*.ttf"]},
)
