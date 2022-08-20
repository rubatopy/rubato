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
        *cythonize(
            "rubato/**/*.py",
            exclude=["rubato/__pyinstaller/**/*", "rubato/static/**/*"],
            compiler_directives={
                "embedsignature": True,
                "language_level": 3,
                "linetrace": linetrace,
            },
        ),
        Extension(
            "rubato.c_src.pixel_editor",
            ["rubato/c_src/pixel_editor.py", "rubato/c_src/PixelEditor.cpp"],
            extra_compile_args=["-std=c++14"],
        ),
    ]
)
