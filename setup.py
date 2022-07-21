"""Setup File"""
from setuptools import setup
import os


def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


extra_files = package_files("rubato/static")

if "RUBATO_VERSION_NUMBER" in os.environ:
    setup(version=os.environ["RUBATO_VERSION_NUMBER"], package_data={"rubato": extra_files})
else:
    setup(version="0.0.0.dev0", package_data={"rubato": extra_files})
