"""Setup File"""
from setuptools import Extension, setup
from Cython.Build import cythonize
import os

if "RUBATO_VERSION" in os.environ:
    version = os.environ["RUBATO_VERSION"]
else:
    version = "0.0.0"


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
            "rubato.c_src.pixel_editor",
            ["rubato/c_src/pixel_editor.py", "rubato/c_src/PixelEditor.cpp"],
            extra_compile_args=["-std=c++14"],
            extra_link_args=["-std=c++14"],
        ),
        *cythonize(
            "rubato/**/*.py",
            exclude=["rubato/__pyinstaller/**/*", "rubato/static/**/*", "rubato/c_src/**/*"],
            compiler_directives={
                "embedsignature": True,
                "language_level": 3,
            },
        ),
    ]
)
