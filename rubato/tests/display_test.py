"""Test the Display class."""
from rubato.utils.display import Display
from rubato.utils.vector import Vector


def test_properties(rub):
    # pylint: disable=unused-argument, comparison-with-callable
    assert Display.window_size == Vector(200, 100)
    assert Display.res == Vector(400, 200)
    assert Display.window_pos == Vector(0, 0)
