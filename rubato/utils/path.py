"""Path helper method for finding relative paths."""
import sys, os


def get_path(rel_path: str) -> str:
    """
    Gets the absolute path of a relative path.

    Args:
        rel_path: The relative path.

    Returns:
        The absolute path.
    """
    try:
        return os.path.join(sys._MEIPASS, rel_path)  # type: ignore
    except AttributeError:
        return os.path.abspath(rel_path)
