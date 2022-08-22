"""Setup File"""
from setuptools import Extension, setup
from Cython.Build import cythonize
import os

if "RUBATO_VERSION" in os.environ:
    version = os.environ["RUBATO_VERSION"]
else:
    version = "0.0.0"

if "TEST_MODE" in os.environ:
    linetrace = os.environ["TEST_MODE"] == "1"
else:
    linetrace = False

if "CYTHONIZE_CDRAW" in os.environ:
    cdraw = os.environ["CYTHONIZE_CDRAW"] == "1"
else:
    cdraw = False


def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


setup(
    version=version,
    package_data={"rubato": package_files("rubato/static")},
    ext_modules=[
        Extension(
            "rubato.c_src.c_draw",
            ["rubato/c_src/c_draw.py", "rubato/c_src/cdraw.cpp"],
            extra_compile_args=["-std=c++14"],
        ),
        *cythonize(
            "rubato/**/*.py",
            exclude=["rubato/__pyinstaller/**/*", "rubato/static/**/*"] + (["rubato/c_src/**/*"] if cdraw else []),
            compiler_directives={
                "embedsignature": True,
                "language_level": 3,
                "linetrace": linetrace,
            },
        ),
    ]
)
