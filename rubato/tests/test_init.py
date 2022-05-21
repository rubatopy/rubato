"""Test the initialization of Rubato."""
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
    monkeypatch.setattr(rubato.Game, "constant_loop", loop)
    rubato.begin()
    loop.assert_called_once()  # This code is reachable because of the monkeypatch


# @pytest.mark.rub
# def test_init(monkeypatch):
#     assert rubato.Game.initialized is False
#     rubato.init({"target_fps": 0})
