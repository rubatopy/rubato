"""Test the Game class"""
import pytest
from unittest.mock import Mock
from rubato.game import Game
from rubato.struct.scene import Scene
from rubato.utils.error import InitError, IdError, PrintError
# pylint: disable=redefined-outer-name, unused-argument, protected-access


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


def test_init():
    with pytest.raises(InitError):
        Game()


def test__add():
    with pytest.raises(IdError):
        Game._add(Scene(name="scene"))
        Game._add(Scene(name="scene"))


@pytest.mark.rub
def test_quit(rub):
    with pytest.raises(SystemExit):
        Game.quit()
    assert Game.state == Game.STOPPED


def test_start(monkeypatch):
    loop = Mock()
    monkeypatch.setattr(Game, "loop", loop)
    Game.start()
    loop.assert_called_once()

    loop = Mock(side_effect=KeyboardInterrupt)
    quit_mock = Mock()
    monkeypatch.setattr(Game, "quit", quit_mock)
    monkeypatch.setattr(Game, "loop", loop)
    Game.start()
    quit_mock.assert_called_once()

    loop = Mock(side_effect=PrintError)

    assert Game.state == Game.RUNNING
    Game.state = Game.STOPPED
