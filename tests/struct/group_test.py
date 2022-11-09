"""Test the Group class."""
from unittest.mock import Mock
import pytest
from rubato.struct.gameobject.physics.hitbox import Hitbox
from rubato.struct.gameobject.game_object import GameObject
from rubato.struct.group import Group
from rubato.utils.error import Error
from rubato.utils.rendering.camera import Camera
# pylint: disable=redefined-outer-name


@pytest.fixture()
def group():
    return Group()


@pytest.fixture()
def go():
    g = GameObject()
    g._update = Mock()
    g._fixed_update = Mock()
    g._draw = Mock()
    return g


def test_init(group):
    assert group.name == ""
    assert group.game_objects == []
    assert group.groups == []
    assert group.active


def test_add(monkeypatch, group, go):
    monkeypatch.setattr("rubato.game.Game.state", 1)
    group.add(go)
    group._dump()
    assert go in group.game_objects

    g = Group()
    group.add(g)
    group._dump()
    assert g in group.groups

    with pytest.raises(Error):
        group.add(group)

    with pytest.raises(ValueError):
        group.add(Camera())


def test_pass_on_funcs(group, go):
    group.add(go)
    g = Group()
    group.add(g)

    group._update()
    c = Camera()
    group._draw(c)

    go._update.assert_called_once()
    go._draw.assert_called_once_with(c)


def test_fixed_update(monkeypatch, group, go):
    go.add(Hitbox())
    go2 = GameObject().add(Hitbox())
    g = Group()
    g.add(go2, go)

    group.add(go, g)

    collide = Mock()
    calc_bb = Mock()
    monkeypatch.setattr("rubato.struct.qtree._QTree.collide", collide)
    monkeypatch.setattr("rubato.struct.qtree._QTree.calc_bb", calc_bb)

    group._fixed_update()

    go._fixed_update.assert_called()
    assert go._fixed_update.call_count == 2

    assert collide.call_count == 5
    assert calc_bb.call_count == 2


def test_count(group):
    assert group.count() == 0

    group.add(*[Group() for _ in range(10)])
    group.add(*[GameObject() for _ in range(10)])

    assert group.count() == 20
