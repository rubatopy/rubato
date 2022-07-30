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


extra_files = package_files("rubato/static")

if "RUBATO_VERSION_NUMBER" in os.environ:
    version = os.environ["RUBATO_VERSION_NUMBER"]
else:
    version = "0.0.0"

setup(
    version=version,
    package_data={"rubato": extra_files},
    ext_modules=cythonize(
        "rubato/**/*.py",
        exclude=["rubato/__pyinstaller/**/*", "rubato/static/**/*"],
        compiler_directives={
            "embedsignature": True,
            "language_level": 3
        },
    ),
)
