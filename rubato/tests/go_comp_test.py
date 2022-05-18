"""Test the Game Object class"""
from unittest.mock import Mock
import pytest
from rubato.classes.camera import Camera
from rubato.classes.components.hitbox import Hitbox, Rectangle
from rubato.classes.game_object import GameObject
from rubato.classes.components.component import Component
from rubato.utils.error import DuplicateComponentError
from rubato.utils.vector import Vector
# pylint: disable=redefined-outer-name


@pytest.fixture()
def go():
    return GameObject({
        "name": "Test",
        "pos": Vector(100, 100),
        "z_index": 1,
        "rotation": 0,
    })


@pytest.fixture()
def comp():
    c = Component({"offset": Vector(1, 1), "rot_offset": 90})
    c.update = Mock()
    c.fixed_update = Mock()
    c.draw = Mock()
    c.setup = Mock()
    c.delete = Mock()
    return c


def test_init(go, comp):
    assert go.name == "Test"
    assert go.pos.x == 100
    assert go.pos.y == 100
    assert go.z_index == 1
    assert go.rotation == 0
    assert not go.debug
    assert go._components == {}  # pylint: disable=protected-access

    assert comp.offset.x == 1
    assert comp.offset.y == 1
    assert comp.rotation_offset == 90
    assert not comp.singular
    assert not comp.gameobj


def test_add(go, comp):
    go.add(comp)

    assert comp.gameobj == go
    assert comp in go._components[Component]  # pylint: disable=protected-access

    comp.singular = True

    with pytest.raises(DuplicateComponentError):
        go.add(comp)

    hb = Hitbox()
    go.add(hb)
    assert hb.gameobj == go
    assert hb in go._components[Hitbox]  # pylint: disable=protected-access


def test_remove(go, comp):
    go.add(comp)
    go.remove(Component)

    with pytest.raises(KeyError):
        assert go._components[Component]  # pylint: disable=protected-access

    with pytest.raises(Warning):
        go.remove(Component)

    go.add(comp)
    go.add(comp)
    assert len(go._components[Component]) == 2  # pylint: disable=protected-access
    go.remove_all(Component)

    with pytest.raises(KeyError):
        assert go._components[Component]  # pylint: disable=protected-access

    with pytest.raises(Warning):
        go.remove_all(Component)


def test_get(go, comp):
    go.add(comp)
    assert go.get(Component) == comp
    assert go.get(Hitbox) is None

    hb = Rectangle({})
    go.add(hb)
    assert go.get(Rectangle) == hb

    go.add(comp)
    go.add(comp)
    go.add(hb)
    assert go.get_all(Component) == [comp, comp, comp]
    assert go.get_all(Rectangle) == [hb, hb]

    go.remove_all(Component)
    assert go.get_all(Component) == []


def test_pass_on_funcs(go, comp):
    go.add(comp)
    go.delete()
    go.setup()
    go.update()
    go.fixed_update()

    comp.delete.assert_called_once()
    comp.setup.assert_called_once()
    comp.update.assert_called_once()
    comp.fixed_update.assert_called_once()


def test_draw(go, comp):
    go.add(comp)
    c = Camera()
    go.draw(c)

    comp.draw.assert_called_once_with(c)

    # TODO test debug draw


def test_comp_funcs():
    comp = Component()

    comp.draw(Camera())
    comp.update()
    comp.fixed_update()
    comp.delete()
    comp.setup()

    new = comp.clone()
    assert new.offset == comp.offset
    assert new.rotation_offset == comp.rotation_offset
    assert new.singular == comp.singular
    assert new.gameobj == comp.gameobj
    assert new is not comp
