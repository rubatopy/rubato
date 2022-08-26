"""A simple path helper for managing relative paths."""
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
        return os.path.join(sys._MEIPASS, rel_path)  # type: ignore # pylint: disable=protected-access
    except AttributeError:
        return os.path.abspath(rel_path)
