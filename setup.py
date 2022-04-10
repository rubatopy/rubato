# pylint: disable=all
from setuptools import setup, find_packages

VERSION = "2.0.0"
DESCRIPTION = "A lightweight, developer-first game engine built for Python."
LONG_DESCRIPTION = (open("README.md").read() + "\n\n" + open("CHANGELOG.md").read())

REQUIREMENTS = ["PySDL2==0.9.11"]

ADVANCED_REQUIREMENTS = ["numpy==1.22.3", "opensimplex==0.4.2"]

DEV_REQUIREMENTS = ["pylint==2.12.2", "yapf==0.32.0"]

setup(
    name="rubato",
    version=VERSION,
    author="Martin Chaperot, Yamm Elnekave, Tomer Sedan",
    author_email="m.artin.chapino@gmail.com",
    license="GPL-3.0",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/rubatopy/rubato",
    packages=find_packages(where=".", include=["rubato*"]),
    install_requires=REQUIREMENTS,
    extras_require={
        "advanced": ADVANCED_REQUIREMENTS,
        "dev": DEV_REQUIREMENTS,
    },
    python_requires=">=3.10",
    package_data={"rubato": ["static/fonts/*.ttf", "static/png/*.png"]},
)
