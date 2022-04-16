"""The hooks init for PyInstaller."""  # pylint: disable=invalid-name
import os


def get_hook_dirs():
    return [os.path.dirname(__file__)]
