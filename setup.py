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

setup(package_data={"rubato": extra_files})
