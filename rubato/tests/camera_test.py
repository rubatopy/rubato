"""Test the Camera class"""
from unittest.mock import Mock
from rubato.classes.camera import Camera
from rubato.utils.radio import Radio


def test_init():
    c = Camera()
    assert c.pos.x == 0
    assert c.pos.y == 0
    assert c._zoom == 1  # pylint: disable=protected-access
    assert c.z_index == 100


def test_zoom_prop():
    callback = Mock()
    c = Camera()
    Radio.listen("ZOOM", callback)

    assert c.zoom == 1
    c.zoom = 2
    assert c.zoom == 2

    callback.assert_called_once_with({"camera": c})


def test_transform():
    # TODO once we figure out how to test SDL things
    assert True


def test_scale():
    c = Camera()
    assert c.scale(1) == 1
    assert c.scale(4) == 4
    c.zoom = 4
    assert c.scale(1) == 4
    assert c.scale(4) == 16
