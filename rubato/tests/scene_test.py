"""Test the Scene classes"""
from unittest.mock import Mock
import pytest
from rubato.classes.game_object import GameObject

from rubato.classes.scene import Scene
from rubato.game import Game
# pylint: disable=redefined-outer-name


@pytest.fixture()
def scene():
    yield Scene("test")
    Game.scenes.remove("test")


def test_init(scene: Scene):
    assert scene.root.name == "root"
    assert scene.ui.name == "ui"
    assert scene.id == "test"
    assert Game.scenes._current == scene.id  # pylint: disable=protected-access


def test_scene_add_and_delete(monkeypatch, scene: Scene):
    add = Mock()
    delete = Mock()
    monkeypatch.setattr("rubato.classes.group.Group.add", add)
    monkeypatch.setattr("rubato.classes.group.Group.delete", delete)

    go = GameObject()
    scene.add(go)
    add.assert_called_once_with(go)
    scene.delete(go)
    delete.assert_called_once_with(go)

    add.reset_mock()
    delete.reset_mock()

    scene.add_ui(go)
    add.assert_called_once_with(go)
    scene.delete_ui(go)
    delete.assert_called_once_with(go)


def test_loops(monkeypatch, scene: Scene):
    draw = Mock()
    update = Mock()
    fixed = Mock()
    setup = Mock()

    monkeypatch.setattr("rubato.classes.group.Group.draw", draw)
    monkeypatch.setattr("rubato.classes.group.Group.update", update)
    monkeypatch.setattr("rubato.classes.group.Group.fixed_update", fixed)
    monkeypatch.setattr("rubato.classes.group.Group.setup", setup)

    scene.private_draw()
    scene.private_update()
    scene.private_fixed_update()
    scene.private_setup()

    assert draw.call_count == 2
    assert update.call_count == 2
    assert fixed.call_count == 2
    assert setup.call_count == 2


def test_paused_update(scene: Scene):
    assert not scene.paused_update()
