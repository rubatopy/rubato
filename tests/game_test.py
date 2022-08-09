"""Test the Game class"""
import pytest

from rubato.game import Game
from rubato.struct.scene import Scene
# pylint: disable=redefined-outer-name


@pytest.fixture
def scene():
    return Scene()


def test_state():
    assert Game.state == Game.STOPPED
    Game.state = Game.RUNNING
    assert Game.state == Game.RUNNING
    Game.state = Game.STOPPED
    assert Game.state == Game.STOPPED


def test_camera():
    Scene()
    assert Game.camera == Game.current.camera
