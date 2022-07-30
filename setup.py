"""Setup File"""
from setuptools import setup
import os
from Cython.Build import cythonize


def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths

setup(
    version=os.environ.get("RUBATO_VERSION_NUMBER", "0.0.0"),
    package_data={
        "rubato": package_files("rubato/static")
    },
    ext_modules=cythonize(
        "rubato/**/*.py",
        exclude=["rubato/__pyinstaller/**/*", "rubato/static/**/*"],
        compiler_directives={
            "embedsignature": True,
            "language_level": 3
        },
    ),
)
