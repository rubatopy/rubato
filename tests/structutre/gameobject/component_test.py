"""Tests for the componet class"""
from unittest.mock import Mock
import pytest
from rubato.structure.gameobject.component import Component
from rubato.structure.gameobject.game_object import GameObject
from rubato.utils.computation.vector import Vector
# pylint: disable=redefined-outer-name


@pytest.fixture
def comp():
    GameObject().add(c := Component(Vector(0, 0), 0, 0, False))
    return c


def test_props(comp):
    assert comp.true_z() == 0
    assert comp.true_pos() == Vector(0, 0)
    assert comp.true_rotation() == 0

    comp.z_index = 1
    comp.gameobj.z_index = 5
    assert comp.true_z() == 6

    comp.rot_offset = 90
    comp.gameobj.rotation = 90
    assert comp.true_rotation() == 180

    comp.offset = Vector(1, 1)
    comp.gameobj.pos = Vector(1, 1)
    assert comp.true_pos() == (2, 0)


def test_update(comp):
    comp.setup = Mock()
    comp.update = Mock()
    comp._update()
    comp._update()
    comp.setup.assert_called_once()
    comp.update.assert_called()
    assert comp.update.call_count == 2


def test_clone(comp):
    comp2 = comp.clone()
    assert comp2.offset == comp.offset
    assert comp2.rot_offset == comp.rot_offset
    assert comp2.z_index == comp.z_index
    assert comp2.hidden == comp.hidden
    assert comp2.singular == comp.singular
    assert comp != comp2


def test_repr(comp):
    assert repr(comp) == "Component(offset=<0.0, 0.0>, rot_offset=0.0, z_index=0, hidden=False)"


def test_str(comp):
    assert str(comp) == f"<Component with GameObject '' at {hex(id(comp))}>"
    delattr(comp, "gameobj")
    assert str(comp) == f"<Component with no GameObject at {hex(id(comp))}>"
