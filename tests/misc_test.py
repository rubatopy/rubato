"""Test the misc file"""
from unittest.mock import Mock
from pytest import MonkeyPatch, raises
from rubato.game import Game
from rubato.misc import world_mouse, wrap
from rubato.struct.gameobject.component import Component
from rubato.struct.gameobject.game_object import GameObject
from rubato.struct.scene import Scene
from rubato.utils.camera import Camera
from rubato.utils.display import Display
from rubato.utils.rb_input import Input
from rubato.utils.vector import Vector


def test_world_mouse(monkeypatch: MonkeyPatch):
    mouse = Mock(return_value=Vector(0, 0))
    monkeypatch.setattr(Input, "get_mouse_pos", mouse)
    Scene()
    monkeypatch.setattr(Game, "camera", None)
    assert Vector(0, 0) == world_mouse()
    monkeypatch.setattr(Game, "camera", Camera(Vector(2, 2), 2))
    monkeypatch.setattr(Display, "center", Vector(1, 1))
    assert Vector(1.5, 1.5) == world_mouse()


def test_wrap(monkeypatch: MonkeyPatch):
    add = Mock()
    c1 = Component()
    monkeypatch.setattr(GameObject, "add", add)
    go1 = wrap(c1)

    assert isinstance(go1, GameObject)
    add.assert_called_once_with(c1)
    add.reset_mock()

    wrap([c1, c1])

    add.assert_called_once_with(c1, c1)

    with raises(TypeError):
        wrap(1)  # type: ignore
