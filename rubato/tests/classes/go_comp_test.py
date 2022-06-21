"""Test the Game Object class"""
from unittest.mock import Mock, call
import pytest
from rubato.classes.camera import Camera
from rubato.classes.components.hitbox import Hitbox, Rectangle
from rubato.classes.game_object import GameObject
from rubato.classes.components.component import Component
from rubato.misc import wrap
from rubato.utils.error import DuplicateComponentError
from rubato.utils.vector import Vector
from rubato.utils.color import Color
# pylint: disable=redefined-outer-name


@pytest.fixture()
def go():
    return GameObject(
        name="Test",
        pos=Vector(100, 100),
        z_index=1,
        rotation=0,
    )


@pytest.fixture()
def comp():
    c = Component(offset=Vector(1, 1), rot_offset=90, z_index=2)
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

    hb = Rectangle()
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
    go.update()
    go.fixed_update()

    comp.delete.assert_called_once()
    comp.update.assert_called_once()
    comp.fixed_update.assert_called_once()


@pytest.mark.rub
def test_draw(monkeypatch, go, comp, rub):
    # pylint: disable=unused-argument
    go.add(comp)
    c = Camera()
    draw_line = Mock()
    monkeypatch.setattr("rubato.utils.draw.Draw.line", draw_line)

    go.debug = True
    go.draw(c)

    comp.draw.assert_called()

    p1 = Vector(110, 100)
    p2 = Vector(90, 100)

    p3 = Vector(100, 110)
    p4 = Vector(100, 90)

    draw_line.assert_has_calls([call(p1, p2, Color(0, 255), 4), call(p3, p4, Color(0, 255), 4)])


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


def test_true_z(go, comp):
    go.add(comp)
    assert comp.true_z == 3


def test_wrap(comp):
    new_go = wrap(comp, name="Test", pos=Vector(100, 100), rotation=0, z_index=1)
    assert new_go.name == "Test"
    assert new_go.pos.x == 100
    assert new_go.pos.y == 100
    assert new_go.z_index == 1
    assert new_go.rotation == 0
    assert not new_go.debug
    assert new_go.get(type(comp)) == comp
