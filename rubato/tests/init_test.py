"""Test the initialization of Rubato."""
from importlib.resources import files
from unittest.mock import Mock
import pytest
import rubato
import sdl2


@pytest.mark.rub
def test_state_controls(monkeypatch, rub):
    # pylint: disable=unused-argument
    assert rubato.Game.state == rubato.Game.STOPPED
    rubato.resume()
    assert rubato.Game.state == rubato.Game.RUNNING
    rubato.pause()
    assert rubato.Game.state == rubato.Game.PAUSED
    rubato.end()
    assert rubato.Game.state == rubato.Game.STOPPED


def test_begin_uninit():
    with pytest.raises(RuntimeError):
        rubato.begin()


@pytest.mark.rub
def test_begin_init(monkeypatch, rub):
    # pylint: disable=unused-argument
    assert rubato.Game.state == rubato.Game.STOPPED
    loop = Mock()
    monkeypatch.setattr(rubato.Game, "constant_loop", loop)
    rubato.begin()
    loop.assert_called_once()  # This code is reachable because of the monkeypatch


@pytest.mark.rub
def test_init(monkeypatch):
    set_icon = Mock()
    monkeypatch.setattr(rubato.Display, "set_window_icon", set_icon)

    assert rubato.Game.initialized is False
    rubato.init(
        name="Untitled Game",
        window_size=rubato.Vector(360, 360),
        res=rubato.Vector(1080, 1080),
        target_fps=60,
        physics_fps=30,
        border_color=rubato.Color(0, 0, 0),
        background_color=rubato.Color(255, 255, 255),
        icon="",
        hidden=False,
    )
    assert rubato.Game.initialized is True
    assert rubato.Game.state == rubato.Game.STOPPED
    assert rubato.Game.border_color == rubato.Color(0, 0, 0)
    assert rubato.Game.background_color == rubato.Color(255, 255, 255)

    assert rubato.Time.target_fps == 60
    assert rubato.Time.capped
    assert rubato.Time.normal_delta == 1000 / 60
    assert rubato.Time.physics_fps == 30

    set_icon.assert_called_once_with(files("rubato.static.png").joinpath("logo_filled.png"))
    set_icon.reset_mock()
    sdl2.SDL_Quit()
    rubato.init(
        name="Untitled Game",
        window_size=rubato.Vector(360, 360),
        res=rubato.Vector(1080, 1080),
        target_fps=60,
        physics_fps=30,
        border_color=rubato.Color(0, 0, 0),
        background_color=rubato.Color(255, 255, 255),
        icon=files("rubato.static.png").joinpath("logo_filled.ico"),
        hidden=True,
    )
    set_icon.assert_called_once_with(files("rubato.static.png").joinpath("logo_filled.ico"))
