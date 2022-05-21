"""Test the Game class"""
from unittest.mock import Mock
import pytest, sdl2

from rubato.game import Game
from rubato.classes.scene import Scene
from rubato.utils.radio import Radio

# pylint: disable=redefined-outer-name


@pytest.fixture
def scene():
    return Scene()


def test_state(monkeypatch):
    assert Game.state == Game.STOPPED
    Game.state = Game.RUNNING
    assert Game.state == Game.RUNNING

    push_event = Mock()
    monkeypatch.setattr("sdl2.SDL_PushEvent", push_event)

    Game.state = Game.STOPPED
    assert Game.state == Game.STOPPED
    push_event.assert_called_once()


def test_camera(scene):
    # pylint: disable=unused-argument
    Game.scenes.add(scene, "main")
    assert Game.camera == Game.scenes.current.camera


@pytest.mark.rub
def test_update(rub):
    # pylint: disable=unused-argument
    sdl2.SDL_PushEvent(sdl2.SDL_Event(sdl2.SDL_WINDOWEVENT_RESIZED))

    def resize():
        print("resize")
        assert True

    Radio.listen("RESIZE", resize)
    Game.update()
    pass  # TODO: Finish this test
