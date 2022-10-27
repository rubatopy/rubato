"""Test the Camera class"""
import pytest
from rubato.utils.computation.rb_math import Math
from rubato.utils.computation.vector import Vector
from rubato.utils.hardware.display import Display
from rubato.utils.rendering.camera import Camera


@pytest.mark.rub
def test_init(rub):
    # pylint: disable=unused-argument
    c = Camera()
    assert c.pos == Display.center  # pylint: disable=comparison-with-callable
    assert c._zoom == 1
    assert c.z_index == Math.INF


@pytest.mark.rub
def test_transform(rub):
    # pylint: disable=unused-argument
    c = Camera()
    assert c.transform(Vector(0, 0)) == Vector(0, 0)
    assert c.transform(Vector(100, 100)) == Vector(100, 100)
    c.zoom = 2
    assert c.transform(Vector(0, 0)) == Vector(0, 0)
    assert c.transform(Vector(100, 100)) == Vector(200, 200)
