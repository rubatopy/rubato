"""Path helper method for finding relative paths."""
import sys, os


def get_path(path: str) -> str:
    """
    Gets the absolute path of a relative path.

    Args:
        path: The relative path.

    Returns:
        The absolute path.
    """
    try:
        return os.path.join(sys._MEIPASS, path)  # type: ignore
    except AttributeError:
        return os.path.abspath(path)
