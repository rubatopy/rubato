"""Test the Group class."""
from unittest.mock import Mock
import pytest
from rubato.classes.camera import Camera
from rubato.classes.components.hitbox import Hitbox
from rubato.classes.game_object import GameObject
from rubato.classes.group import Group
from rubato.utils.error import Error
# pylint: disable=redefined-outer-name


@pytest.fixture()
def group():
    return Group()


@pytest.fixture()
def go():
    g = GameObject()
    g.update = Mock()
    g.fixed_update = Mock()
    g.draw = Mock()
    g.delete = Mock()
    g.setup = Mock()
    return g


def test_init(group):
    assert group.name == ""
    assert group.game_objects == []
    assert group.groups == []
    assert group.z_index == 0


def test_add(monkeypatch, group, go):
    monkeypatch.setattr("rubato.classes.group.Game._state", 1)
    group.add(go)
    assert go in group.game_objects

    g = Group()
    group.add(g)
    assert g in group.groups

    with pytest.raises(Error):
        group.add(group)

    with pytest.raises(ValueError):
        group.add(Camera())


def test_delete(group, go):
    group.add(go)
    group.delete(go)
    assert go not in group.game_objects

    g = Group()
    group.add(g)
    group.delete(g)
    assert g not in group.groups

    with pytest.raises(ValueError):
        group.delete(g)


def test_pass_on_funcs(group, go):
    group.add(go)
    g = Group()
    group.add(g)

    group.setup()
    group.update()
    c = Camera()
    group.draw(c)

    go.setup.assert_called_once()
    go.update.assert_called_once()
    go.draw.assert_called_once_with(c)


def test_fixed_update(monkeypatch, group, go):
    go.add(Hitbox())
    go2 = GameObject().add(Hitbox())
    g = Group()
    g.add(go2, go)

    group.add(go, g)

    collide = Mock()
    monkeypatch.setattr("rubato.classes.group.Engine.collide", collide)

    group.fixed_update()

    go.fixed_update.assert_called()
    assert go.fixed_update.call_count == 2
    go.fixed_update.assert_called()
    assert collide.call_count == 3


def test_count(group, go):
    assert group.count() == 0
    g = Group()
    g.add(go)
    assert [group.add(g) for _ in range(10)]
    assert [group.add(go) for _ in range(10)]

    assert group.count() == 20
