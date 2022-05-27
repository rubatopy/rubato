"""Test the SceneManager class"""
from unittest.mock import Mock
import pytest
from rubato.classes.scene import Scene
from rubato.classes.scene_manager import SceneManager
from rubato.utils.error import IdError


def test_starting():
    SceneManager.scenes = {}
    SceneManager._current = ""  # pylint: disable=protected-access
    assert SceneManager.is_empty()

    assert not SceneManager.current


def test_add_and_remove():
    Scene()

    with pytest.raises(IdError):
        Scene()

    assert SceneManager.current.id == "default"

    SceneManager.remove("default")
    assert SceneManager.is_empty()

    s = Scene()
    SceneManager.remove(s)
    assert SceneManager.is_empty()

    with pytest.raises(IdError):
        SceneManager.remove("default")


def test_loops(monkeypatch):
    updates = Mock()
    monkeypatch.setattr("rubato.classes.scene.Scene.update", updates)
    monkeypatch.setattr("rubato.classes.scene.Scene.fixed_update", updates)
    monkeypatch.setattr("rubato.classes.scene.Scene.draw", updates)
    monkeypatch.setattr("rubato.classes.scene.Scene.setup", updates)
    monkeypatch.setattr("rubato.classes.scene.Scene.paused_update", updates)

    SceneManager.setup()
    SceneManager.update()
    SceneManager.fixed_update()
    SceneManager.draw()
    SceneManager.paused_update()

    assert updates.call_count == 0

    Scene()
    SceneManager.setup()
    SceneManager.update()
    SceneManager.fixed_update()
    SceneManager.draw()
    SceneManager.paused_update()

    assert updates.call_count == 5

    SceneManager.remove("default")
