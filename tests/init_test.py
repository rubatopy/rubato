"""Test the initialization of Rubato."""
from importlib.resources import files
from unittest.mock import Mock
import pytest
import rubato


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
    monkeypatch.setattr(rubato.Game, "start", loop)
    rubato.Display.hidden = False
    rubato.begin()
    loop.assert_called_once()  # This code is reachable because of the monkeypatch


@pytest.mark.rub
def test_init(monkeypatch):
    set_icon = Mock()
    monkeypatch.setattr(rubato.Display, "set_window_icon", set_icon)

    assert rubato.Game._initialized is False
    rubato.init(
        name="Untitled Game",
        window_size=rubato.Vector(360, 360),
        res=rubato.Vector(1080, 1080),
        target_fps=60,
        physics_fps=30,
        icon="",
        hidden=False,
    )
    assert rubato.Game._initialized is True
    assert rubato.Game.state == rubato.Game.STOPPED

    assert rubato.Time.target_fps == 60
    assert rubato.Time.capped
    assert rubato.Time._normal_delta == 1 / 60
    assert rubato.Time.physics_fps == 30

    set_icon.assert_called_once_with(str(files("rubato.static.png").joinpath("logo_filled.png")))
    set_icon.reset_mock()
    rubato.init(
        name="Untitled Game",
        window_size=rubato.Vector(360, 360),
        res=rubato.Vector(1080, 1080),
        target_fps=60,
        physics_fps=30,
        icon=str(files("rubato.static.png").joinpath("logo_filled.ico")),
        hidden=True,
        fullscreen="desktop",
    )
    set_icon.assert_called_once_with(str(files("rubato.static.png").joinpath("logo_filled.ico")))
